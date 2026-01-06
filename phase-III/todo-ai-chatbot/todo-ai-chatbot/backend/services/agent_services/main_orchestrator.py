"""
Main Orchestrator for the AI Todo Chatbot using OpenAI Agents SDK
"""
from typing import Dict, Any, List
import openai
from agents import Agent, Runner
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.agent_services.conversation_memory_agent import ConversationMemoryAgent
from backend.mcp.tools import TodoTools
from config.settings import settings

class MainOrchestrator:
    """
    Main Orchestrator that coordinates the OpenAI Agents SDK
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.memory_agent = ConversationMemoryAgent(session)
        
        # Initialize OpenAI client with Groq configuration if specified
        self.client = openai.AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )

        # Define the Todo Agent
        self.todo_agent = Agent(
            name="Todo Manager",
            instructions=(
                "You are an AI Todo Chatbot. Your goal is to help users manage their tasks. "
                "You have access to tools for adding, listing, completing, deleting, and updating tasks. "
                "Always confirm actions in a friendly way. "
                "If a user is ambiguous about which task to delete or update, list their tasks first. "
                "The user_id will be provided in the context."
            ),
            tools=[
                self._add_task_tool,
                self._list_tasks_tool,
                self._complete_task_tool,
                self._delete_task_tool,
                self._update_task_tool
            ]
        )

    async def _add_task_tool(self, title: str, description: str = "") -> dict:
        """Add a new task. title is required."""
        return await TodoTools.add_task(self.session, self.current_user_id, title, description)

    async def _list_tasks_tool(self, status: str = "all") -> List[dict]:
        """List tasks. status can be 'all', 'pending', or 'completed'."""
        return await TodoTools.list_tasks(self.session, self.current_user_id, status)

    async def _complete_task_tool(self, task_id: int) -> dict:
        """Mark a task as completed using its ID."""
        return await TodoTools.complete_task(self.session, self.current_user_id, task_id)

    async def _delete_task_tool(self, task_id: int) -> dict:
        """Delete a task using its ID."""
        return await TodoTools.delete_task(self.session, self.current_user_id, task_id)

    async def _update_task_tool(self, task_id: int, title: str = None, description: str = None) -> dict:
        """Update a task's title or description."""
        return await TodoTools.update_task(self.session, self.current_user_id, task_id, title, description)

    async def handle_request(self, user_id: str, user_message: str, conversation_id: int = None) -> Dict[str, Any]:
        """
        Main entry point to handle a user request using OpenAI Agents SDK Runner
        """
        self.current_user_id = user_id
        
        # 1. Get conversation history
        history = await self.memory_agent.fetch_history(user_id, conversation_id)

        # Ensure we have a conversation if none was provided
        if not conversation_id:
            conv_res = await self.memory_agent.create_conversation(user_id)
            conversation_id = conv_res["conversation_id"]

        # 2. Store user message in database
        await self.memory_agent.append_message(user_id, conversation_id, "user", user_message)

        # 3. Build message array for agent
        messages = history + [{"role": "user", "content": user_message}]

        # 4. Run the Agent using the Runner
        # We use the Runner from openai-agents to handle the tool calling loop
        runner = Runner(
            client=self.client,
            model=settings.openai_model
        )
        
        result = await runner.run(
            agent=self.todo_agent,
            messages=messages
        )

        final_response = result.final_message
        tool_calls_info = [] # Extract tool calls if needed for the response

        # 5. Store assistant response in database
        await self.memory_agent.append_message(user_id, conversation_id, "assistant", final_response)

        # 6. Extract tool calls for the response
        # In a real scenario, you'd iterate through result.messages to find tool calls
        for msg in result.messages:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_info.append({
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    })

        return {
            "conversation_id": conversation_id,
            "response": final_response,
            "tool_calls": tool_calls_info
        }