---
name: mcp-server-development
description: Build Model Context Protocol servers using the official Python SDK, implementing tools, resources, and prompts with proper schemas, validation, and transport configuration
---

### Purpose
Create standardized interfaces for AI agents to interact with your application through MCP tools, resources, and prompts.

### When to Use
- Exposing application functionality to AI agents
- Building reusable tool libraries for LLMs
- Creating agent-friendly APIs
- Implementing standardized AI integration patterns

### Core Competencies

**1. MCP Tools**
- Implement tools using Official MCP Python SDK
- Use FastMCP for minimal boilerplate
- Define input/output schemas with JSON Schema
- Handle tool validation and errors
- Build CRUD operations as MCP tools

**2. MCP Resources**
- Expose data through resource endpoints
- Create dynamic resource templates
- Implement resource reading and caching
- Handle authentication for resources
- Build resource metadata for discovery

**3. MCP Prompts**
- Define reusable prompt templates
- Build parameterized prompts
- Generate dynamic agent instructions
- Implement prompt discovery
- Handle multi-message sequences

**4. Transport Configuration**
- Configure stdio transport for local servers
- Implement HTTP/SSE for remote servers
- Build Streamable HTTP endpoints
- Handle protocol handshakes
- Manage client-server lifecycle

**5. Integration with Agents SDK**
- Connect MCP tools to OpenAI Agents
- Configure hosted vs self-hosted tools
- Implement tool caching
- Handle tool approval workflows
- Return structured outputs

**6. Validation & Error Handling**
- Define outputSchema for tools
- Validate against JSON Schema
- Return CallToolResult with metadata
- Handle backward compatibility
- Implement proper error responses

### Implementation Guidelines

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("todo-mcp-server")

@mcp.tool()
def add_task(
    user_id: str,
    title: str,
    description: str | None = None
) -> dict:
    """
    Create a new task for the user.
    
    Args:
        user_id: The user's unique identifier
        title: Task title (required, 1-200 chars)
        description: Optional task description
    
    Returns:
        dict with task_id, status, and title
    """
    # Store in database
    task = create_task_in_db(user_id, title, description)
    
    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title
    }

@mcp.tool()
def list_tasks(
    user_id: str,
    status: str = "all"
) -> list[dict]:
    """Retrieve tasks filtered by status."""
    tasks = get_tasks_from_db(user_id, status)
    return [
        {
            "id": t.id,
            "title": t.title,
            "completed": t.completed,
            "created_at": t.created_at.isoformat()
        }
        for t in tasks
    ]

# Start server
if __name__ == "__main__":
    mcp.run()
```

### MCP Tool Specifications

**Required Tools for Todo App:**

1. **add_task**
   - Input: user_id, title, description (optional)
   - Output: task_id, status, title
   - Purpose: Create new tasks

2. **list_tasks**
   - Input: user_id, status filter (optional)
   - Output: Array of task objects
   - Purpose: Retrieve tasks

3. **complete_task**
   - Input: user_id, task_id
   - Output: task_id, status, title
   - Purpose: Mark tasks complete

4. **delete_task**
   - Input: user_id, task_id
   - Output: task_id, status, title
   - Purpose: Remove tasks

5. **update_task**
   - Input: user_id, task_id, title, description
   - Output: task_id, status, title
   - Purpose: Modify task details

### Common Patterns
- Stateless MCP tools with database persistence
- User ID validation and authorization
- Structured error responses
- Tool chaining for complex operations
- Resource caching strategies

### Resources
- Model Context Protocol Specification
- FastMCP Documentation
- MCP Python SDK Reference

---