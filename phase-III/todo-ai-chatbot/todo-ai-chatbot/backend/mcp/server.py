from mcp.server import Server
import mcp.types as types
from backend.mcp.tools import TodoTools
from backend.db.session import engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

# Create the MCP Server
app = Server("todo-management-server")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="add_task",
            description="Create a new task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["user_id", "title"],
            },
        ),
        types.Tool(
            name="list_tasks",
            description="Retrieve tasks from the list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]},
                },
                "required": ["user_id"],
            },
        ),
        types.Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
        types.Tool(
            name="delete_task",
            description="Remove a task from the list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
        types.Tool(
            name="update_task",
            description="Modify task title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    """Handle tool execution requests."""
    if not arguments:
        return [types.TextContent(type="text", text="Error: Missing arguments")]

    async with AsyncSession(engine) as session:
        try:
            if name == "add_task":
                result = await TodoTools.add_task(
                    session, 
                    arguments["user_id"], 
                    arguments["title"], 
                    arguments.get("description", "")
                )
            elif name == "list_tasks":
                result = await TodoTools.list_tasks(
                    session, 
                    arguments["user_id"], 
                    arguments.get("status", "all")
                )
            elif name == "complete_task":
                result = await TodoTools.complete_task(
                    session, 
                    arguments["user_id"], 
                    arguments["task_id"]
                )
            elif name == "delete_task":
                result = await TodoTools.delete_task(
                    session, 
                    arguments["user_id"], 
                    arguments["task_id"]
                )
            elif name == "update_task":
                result = await TodoTools.update_task(
                    session, 
                    arguments["user_id"], 
                    arguments["task_id"],
                    arguments.get("title"),
                    arguments.get("description")
                )
            else:
                return [types.TextContent(type="text", text=f"Error: Tool {name} not found")]

            import json
            return [types.TextContent(type="text", text=json.dumps(result))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

# Entry point for stdio/standard mode
if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    asyncio.run(main())
