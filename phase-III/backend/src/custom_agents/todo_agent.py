import asyncio
import os
import random
from typing import Dict, Any, List
from agents import Agent, Runner, set_tracing_disabled, set_default_openai_api
from agents.mcp import MCPServerStdio
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Disable OpenAI tracing since we're using Gemini
set_tracing_disabled(True)

# Use Chat Completions API instead of Responses API (required for non-OpenAI providers)
set_default_openai_api("chat_completions")

# Patch MCP timeout for faster responses
import mcp.shared.session
import datetime
original_send_request = mcp.shared.session.BaseSession.send_request
async def patched_send_request(self, *args, **kwargs):
    kwargs['request_read_timeout_seconds'] = datetime.timedelta(seconds=30)  # Reduced for faster responses
    return await original_send_request(self, *args, **kwargs)
mcp.shared.session.BaseSession.send_request = patched_send_request


class TodoAgent:
    def __init__(self, user_id: str, db_url: str):
        self.user_id = user_id
        
        # Robust DB URL handling
        # Robust DB URL handling for both local and Vercel
        if db_url.startswith("sqlite:///./"):
            # If on Vercel, sqlite won't work for persistence, but we handle path for completeness
            rel_path = db_url.replace("sqlite:///./", "")
            if os.getenv("VERCEL_REGION"):
                # On Vercel, files are usually in the current working directory or /var/task
                self.db_url = f"sqlite:///{os.path.join(os.getcwd(), rel_path)}"
            else:
                root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                abs_path = os.path.abspath(os.path.join(root_dir, rel_path))
                self.db_url = f"sqlite:///{abs_path}"
        else:
            self.db_url = db_url
            
        # Configure Cerebras via OpenAI compatible endpoint
        self.api_key = os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY environment variable is required")
            
        self.base_url = os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1")
        
        # Create AsyncOpenAI client with timeout for faster responses
        # Using verify=False to avoid SSL issues on Windows
        import httpx
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=httpx.AsyncClient(
                verify=False,
                timeout=30.0  # 30 second timeout for faster responses
            )
        )
        
        # Use faster Cerebras model (llama3.1-8b is much faster than gpt-oss-120b)
        self.model_name = os.getenv("CEREBRAS_MODEL", "llama3.1-8b")
        self.model = OpenAIChatCompletionsModel(
            model=self.model_name,  
            openai_client=self.client
        )

    async def get_mcp_server(self, mcp_script_path: str, mcp_src_dir: str):
        import sys
        print(f"DEBUG: Starting MCP server with script: {mcp_script_path}")
        print(f"DEBUG: MCP source dir: {mcp_src_dir}")
        print(f"DEBUG: Using Python executable: {sys.executable}")
        return MCPServerStdio(
            name="todo-tools-server",
            params={
                "command": sys.executable,
                "args": ["-u", mcp_script_path],
                "env": {
                    **os.environ, 
                    "DATABASE_URL": self.db_url,
                    "PYTHONPATH": mcp_src_dir
                }
            }
        )

    async def get_agent(self, server):
        return Agent(
            name="Todo Assistant",
            instructions=f"""You are a friendly, professional todo assistant. Be concise, direct, and helpful.

YOUR IDENTITY & ROLE:
- You help user manage their tasks.
- NEVER mention the user's ID '{self.user_id}' in your response.
- NEVER show internal labels like 'Title:', 'Answer:', or 'Response:' in your final output.
- CRITICAL: NEVER output JSON, dictionary strings, or tool call arguments (e.g., '{{"user_id": ...}}') in your conversational text.
- Speak naturally to the user.

Quick Actions:
- Add task: use add_task(user_id, title, description)
- List tasks: use list_tasks(user_id, status)
- Complete task: use complete_task(user_id, task_id)
- Delete task: use delete_task(user_id, task_id)
- Update task: use update_task(user_id, task_id, title, description)

SILENT TOOL USE:
- When user mentions a task by NAME for delete/complete/update:
  1. CALL list_tasks(user_id, "all") SILENTLY.
  2. MATCH the name to find the ID.
  3. CALL the action with that ID.
- NEVER tell the user "I'm looking for the task" or "Found it". Just perform the action and confirm.

RESPONSE STYLE:
- Keep it SHORT (1-2 sentences).
- Use emojis sparsely: ✅ 🗑️ 📝 🎯
- ONLY show the final result: "🗑️ Deleted 'buy milk' task!" or "✅ Marked 'clean room' as complete!"
- If the model returns multiple parts, only the relevant human-readable text should be shown.

ALWAYS use user_id '{self.user_id}' for all tool calls.""",
            mcp_servers=[server],
            model=self.model
        )

    async def run(self, message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run the agent with the given message and history.
        Implements exponential backoff retry for rate limit errors.
        """
        import sys
        
        # Path to the MCP server main.py
        if os.getenv("VERCEL_REGION"):
            # On Vercel, paths are relative to the deployment root
            root_dir = os.getcwd()
            # If backend is in a 'backend' folder, root_dir might be one level up or same level
            # We assume monorepo root deployment
            mcp_src_dir = os.path.join(root_dir, "mcp-servers", "todo-tools", "src")
            # If the above fails, try relative to current script in the bundled /var/task
            if not os.path.exists(mcp_src_dir):
                script_dir = os.path.dirname(os.path.abspath(__file__)) # .../backend/src/custom_agents
                mcp_src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))), "mcp-servers", "todo-tools", "src")
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            mcp_src_dir = os.path.join(root_dir, "mcp-servers", "todo-tools", "src")
            
        mcp_script_path = os.path.join(mcp_src_dir, "main.py")
        
        async with await self.get_mcp_server(mcp_script_path, mcp_src_dir) as server:
            agent = await self.get_agent(server)

            # Exponential backoff retry logic (optimized for speed)
            max_retries = 3  # Reduced retries for faster failure
            base_delay = 2  # seconds (faster retry for better UX)
            
            for attempt in range(max_retries):
                try:
                    # Construct full input list from history + current message
                    full_input = (history or []) + [{"role": "user", "content": message}]
                    print(f"DEBUG: Running agent turn (attempt {attempt + 1}) with {len(full_input)} messages...")
                    
                    result = await Runner.run(agent, full_input)
                    print(f"DEBUG: Agent finished turn. Result items: {len(result.new_items)}")
                    
                    # Extract tool calls from result.new_items
                    tool_calls = []
                    for item in result.new_items:
                        # Depending on the SDK version, the structure might vary
                        if hasattr(item, "type") and item.type == "tool_call":
                            # Alternative structure check
                            tc = item
                            tool_calls.append({
                                "name": getattr(tc, "name", "unknown"),
                                "arguments": getattr(tc, "arguments", {})
                            })
                        elif hasattr(item, "type") and item.type == "tool_call_item":
                            tc = item.raw_item
                            if hasattr(tc, "name") and hasattr(tc, "arguments"):
                                tool_calls.append({
                                    "name": tc.name,
                                    "arguments": tc.arguments
                                })
                    
                    print(f"Extracted {len(tool_calls)} tool calls.")
                    
                    # Clean the final output to remove potential noise
                    final_output = result.final_output
                    if final_output:
                        # 1. Strip common hallucinated prefixes
                        prefixes_to_strip = ["Title:", "Response:", "Answer:", "Assistant:", "Result:"]
                        for prefix in prefixes_to_strip:
                            if final_output.lower().startswith(prefix.lower()):
                                final_output = final_output[len(prefix):].strip()
                        
                        # 2. Aggressively remove EVERY JSON-like structure at the start (leaked tool args)
                        import re
                        # Loop to catch multiple consecutive JSON objects (common in multi-step tool calls)
                        while True:
                            # Matches balanced curly braces containing keys like user_id, task_id, etc.
                            json_pattern = r'^\{[^{}]*("user_id"|"task_id"|"title"|"status"|"description")[^{}]*\}\s*'
                            match = re.match(json_pattern, final_output)
                            if match:
                                final_output = final_output[match.end():].strip()
                                print(f"DEBUG: Stripped one JSON block. Remaining: {final_output[:20]}...")
                            else:
                                break
                        
                        # 3. Final safety check for user_id
                        final_output = final_output.replace(self.user_id, "you")
                    
                    try:
                        print(f"DEBUG: Agent Final Output (Cleaned): {final_output}")
                    except UnicodeEncodeError:
                        print("DEBUG: Agent Final Output (Cleaned): [Contains characters not support by console encoding]")
                        
                    return {
                        "response": final_output,
                        "tool_calls": tool_calls
                    }
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"Agent turn failed (attempt {attempt + 1}): {error_msg}")
                    import traceback
                    traceback.print_exc()
                    if attempt == max_retries - 1:
                         raise e
                    # Wait before retrying
                    await asyncio.sleep(base_delay * (2 ** attempt))
            
            # If we get here, all retries failed
            raise Exception("Max retries exceeded due to rate limiting")

    async def run_streamed(self, message: str, history: List[Dict[str, str]] = None):
        """
        Stream the agent response with the given message and history.
        Includes a stream interceptor to hide leaked JSON tool arguments.
        """
        import sys
        import json
        import re
        
        # Path logic (consolidated)
        if os.getenv("VERCEL_REGION"):
            root_dir = os.getcwd()
            mcp_src_dir = os.path.join(root_dir, "mcp-servers", "todo-tools", "src")
            if not os.path.exists(mcp_src_dir):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                mcp_src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))), "mcp-servers", "todo-tools", "src")
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            mcp_src_dir = os.path.join(root_dir, "mcp-servers", "todo-tools", "src")
            
        mcp_script_path = os.path.join(mcp_src_dir, "main.py")
        
        async with await self.get_mcp_server(mcp_script_path, mcp_src_dir) as server:
            agent = await self.get_agent(server)
            full_input = (history or []) + [{"role": "user", "content": message}]
            
            # OpenAI Agents SDK Runner.run_streamed returns a RunResultStreaming object
            result = Runner.run_streamed(agent, full_input)
            
            # Robust Streaming Filter
            full_content_so_far = ""
            yielded_anything = False
            
            async for event in result.stream_events():
                # Intercept text deltas to filter out leaked JSON
                if event.type == "raw_response_event":
                    data = event.data
                    content = ""
                    
                    # Extract content delta
                    if hasattr(data, "delta") and isinstance(data.delta, str):
                        content = data.delta
                    elif hasattr(data, "type") and data.type == "text_delta":
                        content = data.text
                    elif hasattr(data, "choices") and len(data.choices) > 0:
                        choice = data.choices[0]
                        if hasattr(choice, "delta") and hasattr(choice.delta, "content") and choice.delta.content:
                            content = choice.delta.content
                    
                    if content:
                        full_content_so_far += content
                        
                        if not yielded_anything:
                            # Try to find the start of the real message
                            # We strip all balanced { } blocks from the start
                            temp_content = full_content_so_far.strip()
                            
                            while temp_content.startswith("{"):
                                # Find matching }
                                brace_count = 0
                                found_end = -1
                                for i, char in enumerate(temp_content):
                                    if char == "{":
                                        brace_count += 1
                                    elif char == "}":
                                        brace_count -= 1
                                        if brace_count == 0:
                                            found_end = i
                                            break
                                
                                if found_end != -1:
                                    # Skip this block
                                    temp_content = temp_content[found_end + 1:].strip()
                                else:
                                    # Block is incomplete, wait for more chunks
                                    break
                            
                            # If we have non-JSON content left, yield it and mark as done
                            if temp_content and not temp_content.startswith("{"):
                                yielded_anything = True
                                # Update the event data with the cleaned start
                                if hasattr(data, "delta"): data.delta = temp_content
                                elif hasattr(data, "text"): data.text = temp_content
                                elif hasattr(data, "choices"): data.choices[0].delta.content = temp_content
                                yield event
                            
                            # While we haven't yielded anything, we swallow the ongoing JSON leak chunks
                            continue
                
                # Normal event yielding if not filtering
                yield event
