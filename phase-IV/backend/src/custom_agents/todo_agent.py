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

# --- MONKEY PATCH FOR MINIKUBE/DOCKER ---
# Force all httpx.AsyncClient transports to bind to 0.0.0.0 to avoid IPv6 timeouts
import httpx
from httpx import AsyncHTTPTransport

_original_async_transport_init = AsyncHTTPTransport.__init__

def _patched_async_transport_init(self, *args, **kwargs):
    # Force IPv4 binding
    if 'local_address' not in kwargs or kwargs['local_address'] is None:
        kwargs['local_address'] = "0.0.0.0"
    _original_async_transport_init(self, *args, **kwargs)

AsyncHTTPTransport.__init__ = _patched_async_transport_init
print("DEBUG: Monkey-patched AsyncHTTPTransport to force local_address='0.0.0.0'", flush=True)
# ----------------------------------------

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
        
        # Custom httpx client to force IPv4 and handle retries
        import httpx
        from httpx import AsyncHTTPTransport
        
        # Force IPv4 by binding to 0.0.0.0
        # This is CRITICAL for Minikube/Docker environments where IPv6 fails
        transport = AsyncHTTPTransport(retries=3, local_address="0.0.0.0")
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=httpx.AsyncClient(
                transport=transport,
                timeout=httpx.Timeout(90.0, connect=30.0),
                follow_redirects=True
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
        print(f"DEBUG: [Agent] Starting MCP server with command: {sys.executable} -u {mcp_script_path}", flush=True)
        print(f"DEBUG: [Agent] MCP source dir: {mcp_src_dir}", flush=True)
        if not os.path.exists(mcp_script_path):
            print(f"CRITICAL ERROR: [Agent] MCP script NOT FOUND at {mcp_script_path}", flush=True)
            # Try once more with relative to /app (Standard for Docker)
            alt_path = "/app/mcp-servers/todo-tools/src/main.py"
            if os.path.exists(alt_path):
                print(f"DEBUG: [Agent] Found MCP script at alternative path: {alt_path}", flush=True)
                mcp_script_path = alt_path
                mcp_src_dir = "/app/mcp-servers/todo-tools/src"
            else:
                print(f"CRITICAL ERROR: [Agent] All MCP path searches failed.", flush=True)
                raise FileNotFoundError(f"MCP server script not found: {mcp_script_path}")

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

### IDENTITY & ROLE
- Manage tasks efficiently for the user.
- NEVER mention user ID '{self.user_id}' or technical labels in your output.
- CRITICAL: NEVER output JSON or tool call arguments in conversational text.

### BEHAVIOR EXAMPLES
- User: "Add task to buy milk" -> Call add_task(user_id, "Buy milk")
- User: "Show my tasks" -> list_tasks(user_id, "all") -> respond with a clean bulleted list.
- User: "Mark task 3 as done" -> Call complete_task(user_id, 3)
- User: "What's completed?" -> list_tasks(user_id, "completed")

### DUPLICATE PREVENTION
- ALWAYS call list_tasks(user_id, "all") SILENTLY before adding a new task.
- If a similar task exists, don't add it. Say: "🎯 That's already on your list!"

### SILENT ID MATCHING
- For delete/complete/update by NAME:
  1. SILENTLY list_tasks(user_id, "all").
  2. Match name to find ID.
  3. Perform task with ID.
- NEVER describe the searching process. Just confirm the final result.

### RESPONSE STYLE & LIST FORMATTING
- Keep it SHORT (1-2 sentences). Use emojis: ✅ 🗑️ 📝 🎯
- BEAUTIFUL LISTS: ALWAYS use markdown bullet points (-). One task per line.
- STRIP NOISE: NEVER show database IDs (like 31) or redundant statuses (like '- pending') in lists.
- GROUPING: If listing all tasks, group them under headers like **Pending** and **Completed**.
- PREMIUM TONE: Use natural phrases like "Here's what's on your plate: 📝" or "All caught up! ✅"
- EMPTY STATE: If no tasks found, say: "Your list is empty! Ready to add something? 📝"
- Example formatted list:
  **Pending** 📝
  - Buy groceries
  - Call mom
- If task not found, say "Task not found. Try 'show my tasks'."

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
                        prefixes_to_strip = ["Title:", "Response:", "Answer:", "Assistant:", "Result:", "You have the following tasks:"]
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
        import asyncio
        
        # Path logic (consolidated for Docker)
        script_dir = os.path.dirname(os.path.abspath(__file__)) # /app/src/custom_agents/
        app_root = os.path.dirname(os.path.dirname(os.path.dirname(script_dir))) # /app/
        mcp_src_dir = os.path.join(app_root, "mcp-servers", "todo-tools", "src")
        mcp_script_path = os.path.join(mcp_src_dir, "main.py")
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"DEBUG: [Agent] Starting run_streamed attempt {attempt+1}/{max_retries}", flush=True)
                async with await self.get_mcp_server(mcp_script_path, mcp_src_dir) as server:
                    agent = await self.get_agent(server)
                    full_input = (history or []) + [{"role": "user", "content": message}]
                    
                    # Runner.run_streamed returns a RunResultStreaming object
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
                                    temp_content = full_content_so_far.strip()
                                    while temp_content.startswith("{"):
                                        # Find matching }
                                        brace_count = 0
                                        found_end = -1
                                        for i, char in enumerate(temp_content):
                                            if char == "{": brace_count += 1
                                            elif char == "}":
                                                brace_count -= 1
                                                if brace_count == 0:
                                                    found_end = i
                                                    break
                                        if found_end != -1:
                                            temp_content = temp_content[found_end + 1:].strip()
                                        else: break
                                    
                                    if temp_content and not temp_content.startswith("{"):
                                        yielded_anything = True
                                        if hasattr(data, "delta"): data.delta = temp_content
                                        elif hasattr(data, "text"): data.text = temp_content
                                        elif hasattr(data, "choices"): data.choices[0].delta.content = temp_content
                                        yield event
                                    continue
                        
                        # Normal event yielding if not filtering
                        yield event
                
                # If we finish the loop successfully, exit retry loop
                print(f"DEBUG: [Agent] run_streamed completed successfully on attempt {attempt+1}", flush=True)
                return

            except Exception as e:
                print(f"DEBUG: [Agent] run_streamed attempt {attempt+1} failed: {str(e)}", flush=True)
                if attempt < max_retries - 1 and ("Connection error" in str(e) or "ConnectError" in str(e)):
                    print(f"DEBUG: [Agent] Retrying in {retry_delay}s...", flush=True)
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    import traceback
                    traceback.print_exc()
                    raise e
