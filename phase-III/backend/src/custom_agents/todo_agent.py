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
        if db_url.startswith("sqlite:///./"):
            rel_path = db_url.replace("sqlite:///./", "")
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
            instructions=f"""You are a friendly todo assistant for user '{self.user_id}'. Be concise and helpful.

Quick Actions:
- Add task: use add_task(user_id, title, description)
- List tasks: use list_tasks(user_id, status) - status: "all", "pending", or "completed"
- Complete task: use complete_task(user_id, task_id)
- Delete task: use delete_task(user_id, task_id)
- Update task: use update_task(user_id, task_id, title, description)

Response Style:
- Keep responses SHORT and friendly (1-2 sentences max)
- Use emojis for a friendly touch ✅ 📝 🎯
- Confirm actions immediately
- If task not found, suggest listing tasks

ALWAYS use user_id '{self.user_id}' in all tool calls.""",
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
                    print(f"DEBUG: Agent Final Output: {result.final_output}")
                    return {
                        "response": result.final_output,
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
