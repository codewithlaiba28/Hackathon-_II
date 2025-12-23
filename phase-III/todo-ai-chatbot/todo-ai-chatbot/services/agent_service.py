"""
Agent service for the Todo AI Chatbot
Handles interaction with OpenAI Agents SDK and MCP tool calls
"""
from typing import Dict, List, Any
import openai
import os
from ..mcp_servers.todo_management.todo_mcp_server import todo_mcp_server


async def run_agent(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
    """
    Execute the agent runner with the provided messages
    This function would typically interface with OpenAI's Assistants API
    """
    # In a real implementation, this would connect to OpenAI's API
    # For now, we'll simulate the agent behavior with basic logic

    # Check if messages contain task-related commands
    last_user_message = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user_message = msg.get("content", "")
            break

    # Basic response logic (in a real implementation, this would use OpenAI API)
    response_content = await _process_with_openai(messages, user_id)

    return response_content


async def _process_with_openai(messages: List[Dict[str, str]], user_id: str) -> Dict[str, Any]:
    """
    Process messages using OpenAI API
    This would be the actual integration with OpenAI's Assistants API
    """
    # For simulation purposes, I'll return a basic response
    # In a real implementation, this would use the OpenAI API

    # Check if the message contains task-related commands
    last_message = messages[-1] if messages else {"content": ""}
    user_content = last_message.get("content", "")
    user_content_lower = user_content.lower()

    # Simple keyword detection to simulate tool usage
    tool_calls = []
    response_text = "I processed your request."

    if "add " in user_content_lower or "create " in user_content_lower:
        # Extract task description - look for patterns like "add buy milk" or "create task to clean room"
        import re
        # Look for patterns like "add [task description]" or "create [task description]"
        add_patterns = [
            r"(?:add|create|make).*?(?:task|to)?\s+(.+?)(?:\s+and\s+|$)",
            r"(?:add|create|make)\s+(.+?)(?:\s+and\s+|$)"
        ]

        task_description = ""
        for pattern in add_patterns:
            match = re.search(pattern, user_content_lower)
            if match:
                task_description = match.group(1).strip()
                break

        if task_description and task_description != "task":
            # Extract priority if mentioned
            priority = "medium"
            if "high priority" in user_content_lower or "urgent" in user_content_lower or "asap" in user_content_lower:
                priority = "high"
            elif "low priority" in user_content_lower or "not urgent" in user_content_lower:
                priority = "low"

            tool_calls.append({
                "id": "call_" + str(hash(task_description))[:8],
                "type": "function",
                "function": {
                    "name": "add_task",
                    "arguments": f'{{"description": "{task_description}", "user_id": "{user_id}", "priority": "{priority}"}}'
                }
            })
            response_text = f"I've created a task for you: {task_description}"
        else:
            response_text = "I need more information to create a task. Please tell me what you'd like to add."

    elif "list" in user_content_lower or "show" in user_content_lower or "what" in user_content_lower and ("task" in user_content_lower or "todo" in user_content_lower):
        # Determine status filter
        status = "all"
        if "pending" in user_content_lower or "incomplete" in user_content_lower or "not done" in user_content_lower:
            status = "pending"
        elif "completed" in user_content_lower or "done" in user_content_lower or "finished" in user_content_lower:
            status = "completed"

        tool_calls.append({
            "id": "call_list_tasks",
            "type": "function",
            "function": {
                "name": "list_tasks",
                "arguments": f'{{"user_id": "{user_id}", "status": "{status}", "limit": 10}}'
            }
        })

        status_text = status if status != "all" else "all"
        response_text = f"Here are your {status_text} tasks:"

    elif "complete" in user_content_lower or "finish" in user_content_lower or "done" in user_content_lower:
        # Look for task ID or description to complete
        # This is a simplified implementation - in reality, you'd need to identify the specific task
        import re
        # Look for patterns like "complete task 123" or "mark task as complete"
        task_id_match = re.search(r'(?:task|id)\s*(\d+)', user_content_lower)
        if task_id_match:
            task_id = task_id_match.group(1)
            tool_calls.append({
                "id": "call_complete_task",
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "arguments": f'{{"task_id": "{task_id}", "user_id": "{user_id}"}}'
                }
            })
            response_text = f"I've marked task {task_id} as completed."
        else:
            # In a real implementation, we'd need to search for the task by description
            response_text = "I need to know which task to complete. Please specify the task ID or description."

    elif "delete" in user_content_lower or "remove" in user_content_lower:
        # Look for task ID to delete
        import re
        task_id_match = re.search(r'(?:task|id)\s*(\d+)', user_content_lower)
        if task_id_match:
            task_id = task_id_match.group(1)
            tool_calls.append({
                "id": "call_delete_task",
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "arguments": f'{{"task_id": "{task_id}", "user_id": "{user_id}"}}'
                }
            })
            response_text = f"I've deleted task {task_id}."
        else:
            response_text = "I need to know which task to delete. Please specify the task ID or description."

    elif "update" in user_content_lower or "change" in user_content_lower or "modify" in user_content_lower:
        # Look for task ID and new description
        import re
        task_id_match = re.search(r'(?:task|id)\s*(\d+)', user_content_lower)
        if task_id_match:
            task_id = task_id_match.group(1)
            # Extract new description (simplified)
            # This is a basic implementation - real implementation would use NLP
            new_desc = user_content.replace("update", "").replace("change", "").replace("modify", "").replace(task_id, "").strip()
            if new_desc and new_desc != "task":
                tool_calls.append({
                    "id": "call_update_task",
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "arguments": f'{{"task_id": "{task_id}", "user_id": "{user_id}", "description": "{new_desc}"}}'
                    }
                })
                response_text = f"I've updated task {task_id} with the new description."
            else:
                response_text = "I need more information to update the task. Please specify what you'd like to change."

    # In a real implementation, we would call the actual OpenAI API
    # For now, return the simulated response
    return {
        "content": response_text,
        "tool_calls": tool_calls
    }


async def execute_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> Any:
    """
    Execute MCP tools based on agent's tool calls
    """
    # Execute the actual MCP tools using the TodoMCPServer
    try:
        if tool_name == "add_task":
            # Required: description, user_id
            # Optional: due_date, priority
            description = parameters.get("description") or parameters.get("title")
            user_id = parameters.get("user_id")
            due_date = parameters.get("due_date")
            priority = parameters.get("priority")

            if not description:
                return {
                    "status": "error",
                    "message": "Description is required for add_task",
                    "data": None
                }

            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required for add_task",
                    "data": None
                }

            result = await todo_mcp_server.add_task(
                description=description,
                user_id=user_id,
                due_date=due_date,
                priority=priority
            )
            return result

        elif tool_name == "list_tasks":
            # Required: user_id
            # Optional: status, limit
            user_id = parameters.get("user_id")
            status = parameters.get("status")
            limit = parameters.get("limit")

            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required for list_tasks",
                    "data": None
                }

            result = await todo_mcp_server.list_tasks(
                user_id=user_id,
                status=status,
                limit=limit
            )
            return result

        elif tool_name == "complete_task":
            # Required: task_id, user_id
            task_id = parameters.get("task_id")
            user_id = parameters.get("user_id")

            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required for complete_task",
                    "data": None
                }

            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required for complete_task",
                    "data": None
                }

            result = await todo_mcp_server.complete_task(
                task_id=task_id,
                user_id=user_id
            )
            return result

        elif tool_name == "delete_task":
            # Required: task_id, user_id
            task_id = parameters.get("task_id")
            user_id = parameters.get("user_id")

            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required for delete_task",
                    "data": None
                }

            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required for delete_task",
                    "data": None
                }

            result = await todo_mcp_server.delete_task(
                task_id=task_id,
                user_id=user_id
            )
            return result

        elif tool_name == "update_task":
            # Required: task_id, user_id
            # Optional: description, status
            task_id = parameters.get("task_id")
            user_id = parameters.get("user_id")
            description = parameters.get("description")
            status = parameters.get("status")

            if not task_id:
                return {
                    "status": "error",
                    "message": "Task ID is required for update_task",
                    "data": None
                }

            if not user_id:
                return {
                    "status": "error",
                    "message": "User ID is required for update_task",
                    "data": None
                }

            result = await todo_mcp_server.update_task(
                task_id=task_id,
                user_id=user_id,
                description=description,
                status=status
            )
            return result
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to execute tool {tool_name}: {str(e)}",
            "data": None
        }