"""
Main entry point for the Todo Management MCP Server
"""
from fastapi import FastAPI
from todo_management.todo_mcp_server import todo_mcp_server
import uvicorn
import os


app = FastAPI(
    title="Todo Management MCP Server",
    description="Model Context Protocol server for todo management tools",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Todo Management MCP Server", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Example endpoints for testing the MCP tools
@app.post("/add_task")
async def add_task_endpoint(description: str, user_id: str, due_date: str = None, priority: str = "medium"):
    result = await todo_mcp_server.add_task(description, user_id, due_date, priority)
    return result


@app.get("/list_tasks")
async def list_tasks_endpoint(user_id: str, status: str = "pending", limit: int = 10):
    result = await todo_mcp_server.list_tasks(user_id, status, limit)
    return result


@app.post("/complete_task")
async def complete_task_endpoint(task_id: str, user_id: str):
    result = await todo_mcp_server.complete_task(task_id, user_id)
    return result


@app.post("/delete_task")
async def delete_task_endpoint(task_id: str, user_id: str):
    result = await todo_mcp_server.delete_task(task_id, user_id)
    return result


@app.post("/update_task")
async def update_task_endpoint(task_id: str, user_id: str, description: str = None, status: str = None):
    result = await todo_mcp_server.update_task(task_id, user_id, description, status)
    return result


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)