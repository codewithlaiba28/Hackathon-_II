---
name: openai-agents-sdk-development
description: Build sophisticated AI agents using OpenAI Agents SDK with function tools, multi-agent orchestration, context management, guardrails, and structured outputs
---

### Purpose
Create production-ready AI agents that can handle complex workflows, delegate to specialized sub-agents, maintain context, and produce validated structured outputs.

### When to Use
- Building conversational AI applications
- Implementing multi-agent systems with specialized roles
- Creating task management bots with natural language understanding
- Developing agents that need structured data extraction

### Core Competencies

**1. Basic Agent Creation**
- Define agents with custom instructions
- Implement function tools with automatic schema generation
- Configure model settings (temperature, max_tokens, tool_choice)
- Handle agent responses and tool calls
- Implement streaming responses

**2. Multi-Agent Systems**
- Build triage agents for routing queries
- Create expert agents for specific domains
- Implement agent handoffs and delegation
- Design agent collaboration patterns
- Use agent cloning and templates

**3. Context Management**
- Build type-safe context objects
- Implement dependency injection patterns
- Manage user context across runs
- Handle conversation threading
- Access runtime information via context wrappers

**4. Guardrails**
- Implement input validation guardrails
- Create output validation checks
- Build custom safety guardrails
- Configure parallel guardrail execution
- Handle guardrail failures gracefully

**5. Structured Outputs**
- Configure agents to produce Pydantic models
- Extract structured data from conversations
- Validate outputs against schemas
- Handle dataclasses and TypedDict
- Build task parsers with validation

**6. Observability**
- Enable built-in tracing
- Export traces to external platforms
- Debug agent decision-making
- Monitor tool usage and performance
- Visualize agent workflows

### Implementation Guidelines

```python
from agents_sdk import Agent, function_tool
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"

@function_tool
def add_task(title: str, description: str = None) -> dict:
    """Add a new task to the user's todo list."""
    # Implementation
    return {"task_id": 1, "status": "created"}

todo_agent = Agent(
    name="todo_assistant",
    instructions="""You are a helpful todo assistant. 
    Help users manage their tasks through natural language.""",
    model="gpt-4",
    tools=[add_task, list_tasks, complete_task]
)

# Run agent with context
result = todo_agent.run(
    user_message="Add a task to buy groceries",
    context={"user_id": "user123"}
)
```

### Common Patterns
- Triage agent + expert agents architecture
- Context-aware tool execution
- Structured output extraction
- Multi-turn conversations with state
- Error recovery and fallbacks

### Resources
- OpenAI Agents SDK Documentation
- Agent Patterns Guide
- Guardrails Best Practices

---