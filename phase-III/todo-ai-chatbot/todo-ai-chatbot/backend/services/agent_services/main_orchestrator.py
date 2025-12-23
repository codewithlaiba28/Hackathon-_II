"""
Main Orchestrator for the AI Todo Chatbot
Implements the complete agent workflow as specified in the Phase III Design
"""
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from .conversational_agent import ConversationalAgent
from .task_planner_agent import TaskPlannerAgent
from .tool_execution_agent import ToolExecutionAgent
from .conversation_memory_agent import ConversationMemoryAgent


class MainOrchestrator:
    """
    Main Orchestrator that coordinates all agents according to the Phase III Design
    Implements the agent behavior & decision logic
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.conversational_agent = ConversationalAgent()
        self.task_planner_agent = TaskPlannerAgent()
        self.tool_execution_agent = ToolExecutionAgent()
        self.memory_agent = ConversationMemoryAgent(session)

    async def handle_request(self, user_id: str, user_message: str, session_id: str = None) -> Dict[str, Any]:
        """
        Main entry point to handle a user request following the decision logic
        """
        # 1. Get conversation history
        history = await self.memory_agent.fetch_history(user_id, session_id)

        # If no session_id was provided or no conversation exists, create a new one
        if not session_id or not history:
            conversation_result = await self.memory_agent.create_conversation(user_id)
            if not conversation_result["success"]:
                return {
                    "response": "I'm having trouble starting a conversation. Please try again.",
                    "tool_calls": [],
                    "conversation_id": None
                }
            session_id = conversation_result["conversation_id"]

        # 2. Store user message in conversation
        await self.memory_agent.append_message(user_id, session_id, "user", user_message)

        # 3. Process the message through the conversational agent
        conversation_result = self.conversational_agent.process_message(user_message, history)

        if conversation_result["response_type"] == "direct_response":
            # Handle chitchat directly
            response = conversation_result["response"]

            # Store assistant response
            await self.memory_agent.append_message(user_id, session_id, "assistant", response)

            return {
                "response": response,
                "tool_calls": [],
                "conversation_id": session_id
            }
        elif conversation_result["response_type"] == "route_to_planner":
            # Route to Task Planner Agent
            user_request = conversation_result["user_message"]
            intent = conversation_result["intent"]

            # 4. Analyze with Task Planner Agent
            plan = self.task_planner_agent.analyze(user_request, history)

            if plan["is_ambiguous"]:
                # Ask for clarification
                response = f"I need more information: {plan['missing_info']}"

                # Store assistant response
                await self.memory_agent.append_message(user_id, session_id, "assistant", response)

                return {
                    "response": response,
                    "tool_calls": [],
                    "conversation_id": session_id
                }

            # 5. Execute the plan
            results = []
            for step in plan["steps"]:
                # Pre-execution check - resolve dependencies if needed
                # (In this implementation, we'll assume steps can be executed independently)

                # Execute the tool
                result = await self.tool_execution_agent.execute_mcp_tool(
                    tool_name=step["tool"],
                    arguments=step["args"]
                )

                results.append(result)

                # If there's an error that's not recoverable, we might want to stop
                # For now, we'll continue with all steps
                if result["status"] == "error":
                    print(f"Error executing tool {step['tool']}: {result['message']}")

            # 6. Generate final response based on results
            final_response = await self.generate_summary(results, user_request)

            # Store assistant response
            await self.memory_agent.append_message(user_id, session_id, "assistant", final_response)

            # Extract tool calls for the response
            tool_calls = []
            for i, step in enumerate(plan["steps"]):
                tool_calls.append({
                    "id": f"call_{i}",
                    "type": "function",
                    "function": {
                        "name": step["tool"],
                        "arguments": str(step["args"])
                    }
                })

            return {
                "response": final_response,
                "tool_calls": tool_calls,
                "conversation_id": session_id
            }

    async def generate_summary(self, results: List[Dict[str, Any]], user_request: str) -> str:
        """
        Generate a human-readable summary of the tool execution results
        """
        if not results:
            return "I processed your request, but there were no actions to take."

        success_count = sum(1 for r in results if r["status"] == "success")
        error_count = len(results) - success_count

        if error_count == 0:
            # All operations succeeded
            if len(results) == 1:
                result = results[0]
                if result["data"]:
                    if "add_task" in user_request.lower():
                        task = result["data"]
                        return f"I've created the task: '{task.get('description', task.get('title', 'Unknown'))}'"
                    elif "complete_task" in user_request.lower():
                        task = result["data"]
                        return f"I've marked the task as completed: '{task.get('description', task.get('title', 'Unknown'))}'"
                    elif "delete_task" in user_request.lower():
                        return "I've deleted the task successfully."
                    elif "update_task" in user_request.lower():
                        task = result["data"]
                        return f"I've updated the task: '{task.get('description', task.get('title', 'Unknown'))}'"
                    elif "list_tasks" in user_request.lower():
                        tasks = result["data"]
                        if tasks:
                            task_list = [f"- {task.get('description', task.get('title', 'Unknown'))}" for task in tasks]
                            return f"Here are your tasks:\n" + "\n".join(task_list)
                        else:
                            return "You don't have any tasks."
            else:
                return f"I've completed {success_count} actions successfully."
        elif success_count == 0:
            # All operations failed
            error_messages = [r["message"] for r in results if r["status"] == "error"]
            return f"I'm sorry, but I couldn't complete your request. Errors: {', '.join(error_messages)}"
        else:
            # Some operations succeeded, some failed
            return f"I've completed {success_count} out of {len(results)} actions. Some operations encountered issues."