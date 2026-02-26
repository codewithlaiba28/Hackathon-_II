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
        
        # Use Cerebras model from environment (default: llama3.1-8b, recommended: llama-3.3-70b)
        self.model_name = os.getenv("CEREBRAS_MODEL", "llama3.1-8b")
        print(f"DEBUG: TodoAgent using model: {self.model_name}", flush=True)
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
            instructions=f"""You are a helpful todo assistant. Current date: 2026-02-16 (Sunday).

### CORE RULES
- NEVER mention user ID '{self.user_id}' in responses
- NEVER output JSON or tool arguments in your responses
- MANDATORY: Always include a short confirmation text (e.g. "✅ Task added") even after tool calls.
- Keep responses SHORT (1-2 sentences max)

### ADDING TASKS - CRITICAL EXAMPLES
User: "Add buy milk"
→ add_task(user_id, "Buy milk")

User: "Add buy biryani due Tuesday 9pm priority high"
→ add_task(user_id, "Buy biryani", priority="high", due_date="2026-02-18T21:00:00")

User: "Add task buy samosas recurring daily due Feb 20 at 8pm priority high description get from shop"
→ add_task(user_id, "Buy samosas", description="get from shop", priority="high", due_date="2026-02-20T20:00:00", is_recurring=True, recurrence_pattern="daily")

### DATE PARSING - MUST FOLLOW
**⚠️ CRITICAL: IF USER MENTIONS A DATE/TIME, YOU MUST INCLUDE due_date PARAMETER ⚠️**

Quick reference (today = 2026-02-16):
- "Thursday 8pm" → "2026-02-20T20:00:00" (Feb 20 is Thursday)
- "Tuesday 9pm" → "2026-02-18T21:00:00"
- "02/17/2026 9pm" or "Feb 17 9pm" → "2026-02-17T21:00:00"  
- "tomorrow 3pm" → "2026-02-17T15:00:00"
- "Wednesday" (no time) → "2026-02-19T09:00:00"

Time conversions: 9pm=21:00, 8pm=20:00, 7pm=19:00, 3pm=15:00, 10am=10:00

Days this week:
Mon=17, Tue=18, Wed=19, Thu=20, Fri=21, Sat=22, Sun=23

### PRIORITY
- If user says "high/medium/low priority", use that value
- Default: "medium"

### RECURRING TASKS
- If user says "daily/weekly/monthly", set is_recurring=True and recurrence_pattern="daily"/"weekly"/"monthly"

### ⚠️ DUPLICATE CHECK - MANDATORY BEFORE ADDING ⚠️
**YOU MUST FOLLOW THESE STEPS EXACTLY:**

1. BEFORE calling add_task, ALWAYS call list_tasks(user_id, "all") FIRST
2. Check if ANY task has the EXACT SAME title (case-insensitive)
3. If EXACT match found → DO NOT ADD, say "🎯 That's already on your list!"
4. If NO exact match → ADD THE TASK

**Examples:**
- Existing: "Call mom" → User says "call mom" → DON'T ADD (exact match)
- Existing: "Call mom" → User says "Call dad" → ADD IT (different)
- Existing: "Buy milk" → User says "Buy biryani" → ADD IT (different)

**⚠️ NEVER ADD A TASK WITHOUT CHECKING FIRST ⚠️**

### OTHER COMMANDS
- "Show tasks" → list_tasks(user_id, "all")
- "Complete task 5" → complete_task(user_id, 5)
- "Delete task 3" → delete_task(user_id, 3)

### RESPONSE FORMAT
- Use emojis: ✅ 🗑️ 📝 🎯
- Lists: use markdown bullets (-)
- Group by **Pending** and **Completed**
- NEVER show database IDs or technical details

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
        elif os.path.exists("/app/mcp-servers/todo-tools/src"):
            # Docker/Minikube fallback
            mcp_src_dir = "/app/mcp-servers/todo-tools/src"
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
                        import json as json_module
                        # Loop to catch multiple consecutive JSON objects (common in multi-step tool calls)
                        leaked_tool_blocks = []  # Collect leaked tool call JSON for fallback execution
                        while True:
                            # Improved pattern to match leading JSON blocks with tool call keys
                            # Catches blocks starting with { and ending with }
                            if not final_output.startswith('{'):
                                break
                                
                            # Find the matching closing brace for the first open brace
                            stack = 0
                            end_pos = -1
                            for i, char in enumerate(final_output):
                                if char == '{': stack += 1
                                elif char == '}': 
                                    stack -= 1
                                    if stack == 0:
                                        end_pos = i + 1
                                        break
                            
                            if end_pos > 0:
                                # Extract potential JSON block
                                json_block = final_output[:end_pos]
                                # If it contains technical keys, strip it
                                if any(k in json_block for k in ["user_id", "task_id", "title", "arguments", "name", "call_id"]):
                                    print(f"DEBUG: Stripping leaked JSON tool block: {json_block[:80]}...", flush=True)
                                    leaked_tool_blocks.append(json_block)
                                    final_output = final_output[end_pos:].strip()
                                    continue
                            
                            break
                        
                        # 2b. FALLBACK: If LLM leaked tool calls as text (0 proper tool calls extracted),
                        # parse the leaked JSON and execute the tools directly against the DB
                        if not tool_calls and leaked_tool_blocks:
                            fallback_calls = await self._handle_fallback_tool_execution(leaked_tool_blocks)
                            tool_calls.extend(fallback_calls)
                        final_output = final_output.replace(self.user_id, "you")
                        
                        # 4. Fallback if empty but tool calls exist
                        if not final_output.strip() and tool_calls:
                            print("DEBUG: Final output was empty but tool calls exist. Using fallback.", flush=True)
                            # Custom fallback messages based on tool name
                            main_tool = tool_calls[0]["name"]
                            if main_tool == "add_task":
                                final_output = "✅ I've added that task to your list!"
                            elif main_tool == "complete_task":
                                final_output = "✅ Task marked as complete!"
                            elif main_tool == "delete_task":
                                final_output = "🗑️ Task deleted successfully."
                            else:
                                final_output = "✅ Done! I've processed your request."
                    
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


    async def _handle_fallback_tool_execution(self, leaked_tool_blocks: List[str]) -> List[Dict[str, Any]]:
        """
        Parse and execute tools from leaked JSON blocks directly against the database.
        Returns a list of successful tool calls.
        """
        import json as json_module
        import datetime
        from typing import Optional
        
        tool_calls = []
        print(f"DEBUG: Found {len(leaked_tool_blocks)} leaked JSON blocks. Executing fallback...", flush=True)
        
        for block_str in leaked_tool_blocks:
            try:
                # Fix common JSON issues from LLM output
                block_str = block_str.replace("None", "null").replace("True", "true").replace("False", "false")
                block = json_module.loads(block_str)
                
                tool_name = block.get("name", "")
                tool_args = block.get("arguments", block)  # Sometimes the block IS the arguments
                
                # If no "name" key, try to identify the tool from the keys
                if not tool_name:
                    if "title" in tool_args and "task_id" not in tool_args:
                        tool_name = "add_task"
                    elif "task_id" in tool_args and "title" not in tool_args:
                        if "status" in tool_args:
                            tool_name = "complete_task"
                        else:
                            tool_name = "delete_task"
                
                print(f"DEBUG: Fallback executing tool: {tool_name} with args: {tool_args}", flush=True)
                
                # Execute the tool directly using the MCP server's DB functions
                from sqlmodel import Session as SqlSession, select as sql_select, create_engine as sql_create_engine
                fallback_engine = sql_create_engine(self.db_url)
                
                if tool_name == "add_task":
                    user_id_arg = tool_args.get("user_id", self.user_id)
                    title_arg = tool_args.get("title", "Untitled Task")
                    desc_arg = tool_args.get("description")
                    priority_arg = tool_args.get("priority", "medium")
                    due_date_arg = tool_args.get("due_date")
                    is_recurring_arg = tool_args.get("is_recurring", False)
                    recurrence_arg = tool_args.get("recurrence_pattern")
                    
                    # Parse due_date
                    parsed_due = None
                    if due_date_arg:
                        try:
                            parsed_due = datetime.datetime.fromisoformat(str(due_date_arg).strip().replace('Z', '+00:00'))
                        except:
                            pass
                    
                    # Import the Task model from MCP tools inline
                    from sqlmodel import SQLModel, Field as SqlField
                    
                    class FallbackTask(SQLModel, table=True):
                        __tablename__ = "task"
                        __table_args__ = {"extend_existing": True}
                        id: Optional[int] = SqlField(default=None, primary_key=True)
                        user_id: str = SqlField(index=True)
                        title: str
                        description: Optional[str] = SqlField(default=None)
                        status: str = SqlField(default="pending")
                        priority: str = SqlField(default="medium")
                        due_date: Optional[datetime.datetime] = SqlField(default=None)
                        is_recurring: bool = SqlField(default=False)
                        recurrence_pattern: Optional[str] = SqlField(default=None)
                        recurrence_end_date: Optional[datetime.datetime] = SqlField(default=None)
                        parent_recurring_task_id: Optional[int] = SqlField(default=None)
                        reminder_sent: bool = SqlField(default=False)
                        reminder_offset_minutes: int = SqlField(default=0)
                        created_at: datetime.datetime = SqlField(default_factory=datetime.datetime.utcnow)
                        updated_at: datetime.datetime = SqlField(default_factory=datetime.datetime.utcnow)
                    
                    with SqlSession(fallback_engine) as fb_session:
                        new_task = FallbackTask(
                            user_id=self.user_id,
                            title=title_arg,
                            description=desc_arg,
                            status="pending",
                            priority=priority_arg,
                            due_date=parsed_due,
                            is_recurring=is_recurring_arg if is_recurring_arg else False,
                            recurrence_pattern=recurrence_arg if is_recurring_arg else None
                        )
                        fb_session.add(new_task)
                        fb_session.commit()
                        fb_session.refresh(new_task)
                        print(f"DEBUG: Fallback add_task SUCCESS! Task ID: {new_task.id}, Title: {new_task.title}", flush=True)
                        tool_calls.append({"name": "add_task", "arguments": {"title": title_arg}})
                
                elif tool_name == "delete_task":
                    task_id_arg = tool_args.get("task_id")
                    if task_id_arg:
                        with SqlSession(fallback_engine) as fb_session:
                            from sqlmodel import text
                            # Delete tags first
                            fb_session.exec(text(f"DELETE FROM tasktag WHERE task_id = {int(task_id_arg)}"))
                            fb_session.exec(text(f"DELETE FROM task WHERE id = {int(task_id_arg)} AND user_id = '{self.user_id}'"))
                            fb_session.commit()
                            print(f"DEBUG: Fallback delete_task SUCCESS! Task ID: {task_id_arg}", flush=True)
                            tool_calls.append({"name": "delete_task", "arguments": {"task_id": task_id_arg}})
                
                elif tool_name == "complete_task":
                    task_id_arg = tool_args.get("task_id")
                    if task_id_arg:
                        with SqlSession(fallback_engine) as fb_session:
                            from sqlmodel import text
                            fb_session.exec(text(f"UPDATE task SET status = 'completed' WHERE id = {int(task_id_arg)} AND user_id = '{self.user_id}'"))
                            fb_session.commit()
                            print(f"DEBUG: Fallback complete_task SUCCESS! Task ID: {task_id_arg}", flush=True)
                            tool_calls.append({"name": "complete_task", "arguments": {"task_id": task_id_arg}})
                
                elif tool_name == "list_tasks":
                    # list_tasks doesn't need fallback execution - the LLM already has the data
                    print(f"DEBUG: Skipping fallback for list_tasks (read-only)", flush=True)
                
            except Exception as fb_err:
                print(f"DEBUG: Fallback tool execution failed: {str(fb_err)}", flush=True)
                import traceback
                traceback.print_exc()
        
        return tool_calls

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
        
        if os.path.exists("/app/mcp-servers/todo-tools/src"):
            mcp_src_dir = "/app/mcp-servers/todo-tools/src"
        elif os.getenv("VERCEL_REGION"):
            mcp_src_dir = os.path.join(os.getcwd(), "mcp-servers", "todo-tools", "src")
        else:
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
                    tool_calls_extracted = []
                    
                    async for event in result.stream_events():
                        # Track tool calls if they are extraced properly
                        if event.type == "tool_call_item":
                             tc = event.data.raw_item
                             if hasattr(tc, "name") and hasattr(tc, "arguments"):
                                 tool_calls_extracted.append({"name": tc.name, "arguments": tc.arguments})

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

                    # FALLBACK: Check for leaked JSON blocks after stream ends
                    if not tool_calls_extracted and full_content_so_far.strip().startswith("{"):
                        print(f"DEBUG: [Agent] End of stream. Extracting leaked JSON from: {full_content_so_far[:50]}...", flush=True)
                        leaked_blocks = []
                        temp_content = full_content_so_far.strip()
                        while temp_content.startswith("{"):
                            stack = 0
                            end_pos = -1
                            for i, char in enumerate(temp_content):
                                if char == '{': stack += 1
                                elif char == '}':
                                    stack -= 1
                                    if stack == 0:
                                        end_pos = i + 1
                                        break
                            if end_pos > 0:
                                json_block = temp_content[:end_pos]
                                if any(k in json_block for k in ["user_id", "task_id", "title", "arguments", "name", "call_id"]):
                                    leaked_blocks.append(json_block)
                                    temp_content = temp_content[end_pos:].strip()
                                    continue
                            break
                        
                        if leaked_blocks:
                            print(f"DEBUG: [Agent] Executing {len(leaked_blocks)} fallback tool calls after stream.", flush=True)
                            await self._handle_fallback_tool_execution(leaked_blocks)

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
