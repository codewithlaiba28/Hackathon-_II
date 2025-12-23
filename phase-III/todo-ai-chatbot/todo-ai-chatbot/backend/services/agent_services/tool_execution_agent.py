"""
Tool Execution Agent (Executor)
Role: Safely executes MCP tools and handles their immediate outputs.
"""
from typing import Dict, Any
from ...mcp_servers.todo_management.todo_mcp_server import todo_mcp_server


class ToolExecutionAgent:
    """
    Tool Execution Agent (Executor)
    Role: Safely executes MCP tools and handles their immediate outputs.

    Responsibility:
    - Receive specific tool call requests.
    - Validate parameters against MCP spec.
    - Execute the tool.
    - Catch immediate system-level errors (e.g., DB connection retry).

    Skills: validate_args, execute_mcp_tool
    """

    def __init__(self):
        pass

    def validate_args(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skill: Validate Args
        Validates arguments for a specific tool according to the MCP specification.
        """
        validation_result = {
            "is_valid": True,
            "errors": []
        }

        if tool_name == "add_task":
            # Required: description, user_id
            if "description" not in args or not args["description"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Description is required for add_task")

            if "user_id" not in args or not args["user_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("User ID is required for add_task")

            # Optional: due_date, priority
            if "priority" in args and args["priority"] not in ["low", "medium", "high"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Priority must be one of: low, medium, high")

        elif tool_name == "list_tasks":
            # Required: user_id
            if "user_id" not in args or not args["user_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("User ID is required for list_tasks")

            # Optional: status, limit
            if "status" in args and args["status"] not in ["pending", "completed", "all"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Status must be one of: pending, completed, all")

            if "limit" in args and (not isinstance(args["limit"], int) or args["limit"] <= 0):
                validation_result["is_valid"] = False
                validation_result["errors"].append("Limit must be a positive integer")

        elif tool_name == "complete_task":
            # Required: task_id, user_id
            if "task_id" not in args or not args["task_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Task ID is required for complete_task")

            if "user_id" not in args or not args["user_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("User ID is required for complete_task")

        elif tool_name == "delete_task":
            # Required: task_id, user_id
            if "task_id" not in args or not args["task_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Task ID is required for delete_task")

            if "user_id" not in args or not args["user_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("User ID is required for delete_task")

        elif tool_name == "update_task":
            # Required: task_id, user_id
            if "task_id" not in args or not args["task_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Task ID is required for update_task")

            if "user_id" not in args or not args["user_id"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("User ID is required for update_task")

            # At least one optional field must be provided
            optional_fields = ["description", "status"]
            if not any(field in args for field in optional_fields):
                validation_result["is_valid"] = False
                validation_result["errors"].append("At least one field to update (description or status) is required for update_task")

            # Validate status if provided
            if "status" in args and args["status"] not in ["pending", "completed"]:
                validation_result["is_valid"] = False
                validation_result["errors"].append("Status must be one of: pending, completed")

        else:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Unknown tool: {tool_name}")

        return validation_result

    async def execute_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skill: Execute MCP Tool
        The bridge between the Agentic logic and the actual Python function code.

        Input Schema: {"tool_name": "string", "arguments": "dict"}
        Output Schema: {"status": "success" | "error", "data": "any", "message": "string"}
        """
        # Validate arguments first
        validation_result = self.validate_args(tool_name, arguments)
        if not validation_result["is_valid"]:
            return {
                "status": "error",
                "data": None,
                "message": f"Validation failed: {'; '.join(validation_result['errors'])}"
            }

        try:
            # Execute the appropriate tool based on the tool name
            if tool_name == "add_task":
                result = await todo_mcp_server.add_task(
                    description=arguments["description"],
                    user_id=arguments["user_id"],
                    due_date=arguments.get("due_date"),
                    priority=arguments.get("priority", "medium")
                )
            elif tool_name == "list_tasks":
                result = await todo_mcp_server.list_tasks(
                    user_id=arguments["user_id"],
                    status=arguments.get("status"),
                    limit=arguments.get("limit")
                )
            elif tool_name == "complete_task":
                result = await todo_mcp_server.complete_task(
                    task_id=arguments["task_id"],
                    user_id=arguments["user_id"]
                )
            elif tool_name == "delete_task":
                result = await todo_mcp_server.delete_task(
                    task_id=arguments["task_id"],
                    user_id=arguments["user_id"]
                )
            elif tool_name == "update_task":
                result = await todo_mcp_server.update_task(
                    task_id=arguments["task_id"],
                    user_id=arguments["user_id"],
                    description=arguments.get("description"),
                    status=arguments.get("status")
                )
            else:
                return {
                    "status": "error",
                    "data": None,
                    "message": f"Unknown tool: {tool_name}"
                }

            return result

        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "message": f"Failed to execute tool {tool_name}: {str(e)}"
            }