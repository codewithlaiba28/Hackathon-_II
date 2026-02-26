---
name: natural-language-command-processing
description: Build AI agents that understand natural language commands, extract intents and entities, map to tool calls, and provide helpful confirmations and error handling
---

### Purpose
Create conversational interfaces that understand user intent from natural language and translate it into precise tool invocations.

### When to Use
- Building chatbot interfaces
- Implementing voice assistants
- Creating conversational task management
- Developing natural language interfaces for APIs

### Core Competencies

**1. Intent Recognition**
- Parse user intent from messages
- Map intents to MCP tool calls
- Handle ambiguous requests
- Implement clarification dialogs
- Build conversation context awareness

**2. Entity Extraction**
- Extract task titles from messages
- Parse task IDs from natural language
- Identify status filters (pending/completed)
- Extract task attributes (priority, due dates)
- Handle multi-entity requests

**3. Command Mapping**
- Map "add/create/remember" → add_task
- Map "show/list/what's" → list_tasks
- Map "done/complete/finished" → complete_task
- Map "delete/remove/cancel" → delete_task
- Map "change/update/rename" → update_task

**4. Confirmation Generation**
- Provide friendly confirmation messages
- Include task details in responses
- Show what action was taken
- Suggest next actions
- Build conversational flow

**5. Error Handling**
- Handle "task not found" gracefully
- Provide helpful error explanations
- Suggest corrections for failed operations
- Implement fallback responses
- Build multi-turn clarification

**6. Contextual Understanding**
- Maintain conversation history
- Reference previous messages
- Handle pronouns and references
- Build context across turns
- Implement memory of recent actions

### Natural Language Patterns

**Task Creation**
| User Says | Agent Should | Tool Call |
|-----------|--------------|-----------|
| "Add a task to buy groceries" | Extract title | add_task(title="Buy groceries") |
| "I need to remember to pay bills" | Recognize intent | add_task(title="Pay bills") |
| "Create task: call mom" | Parse title | add_task(title="Call mom") |
| "Remind me to exercise tomorrow" | Extract title + context | add_task(title="Exercise tomorrow") |

**Task Listing**
| User Says | Agent Should | Tool Call |
|-----------|--------------|-----------|
| "Show me all my tasks" | List all | list_tasks(status="all") |
| "What's pending?" | Filter pending | list_tasks(status="pending") |
| "What have I completed?" | Filter completed | list_tasks(status="completed") |
| "Show my todo list" | List all | list_tasks(status="all") |

**Task Completion**
| User Says | Agent Should | Tool Call |
|-----------|--------------|-----------|
| "Mark task 3 as complete" | Direct ID reference | complete_task(task_id=3) |
| "I finished the groceries task" | Search then complete | list_tasks() → complete_task() |
| "Done with task 5" | Direct completion | complete_task(task_id=5) |
| "Check off exercise" | Search then complete | list_tasks() → complete_task() |

**Task Deletion**
| User Says | Agent Should | Tool Call |
|-----------|--------------|-----------|
| "Delete task 2" | Direct deletion | delete_task(task_id=2) |
| "Remove the meeting task" | Search then delete | list_tasks() → delete_task() |
| "Cancel the call mom task" | Search then delete | list_tasks() → delete_task() |

**Task Updates**
| User Says | Agent Should | Tool Call |
|-----------|--------------|-----------|
| "Change task 1 to 'Call mom tonight'" | Update with new title | update_task(task_id=1, title="Call mom tonight") |
| "Update the groceries task description" | Multi-turn for details | update_task(task_id=X, description=...) |
| "Rename task 3" | Ask for new name | update_task() after clarification |

### Implementation Guidelines

**Agent Instructions**

```python
todo_agent_instructions = """
You are a helpful todo assistant. Help users manage their tasks through natural language.

# Intent Recognition Rules

## Task Creation
When user mentions: "add", "create", "new task", "remember to", "I need to", "remind me"
→ Call add_task with extracted title

## Task Listing
When user asks: "show", "list", "what's", "my tasks", "todo list"
→ Call list_tasks with appropriate status filter
- "pending", "incomplete", "active" → status="pending"
- "done", "complete", "finished" → status="completed"
- "all", "everything" → status="all"

## Task Completion
When user says: "done", "complete", "finished", "mark as done", "check off"
→ Call complete_task with task_id
- If task_id mentioned directly, use it
- If task name mentioned, search with list_tasks first

## Task Deletion
When user says: "delete", "remove", "cancel", "get rid of"
→ Call delete_task with task_id
- Same search logic as completion

## Task Updates
When user says: "change", "update", "modify", "rename", "edit"
→ Call update_task with task_id and new values

# Response Style
- Always confirm actions: "✅ Added task: Buy groceries"
- Be conversational and friendly
- Ask for clarification when ambiguous
- Suggest related actions when helpful

# Error Handling
- If task not found: "I couldn't find that task. Here are your current tasks..."
- If ambiguous: "I found multiple tasks matching that. Which one? ..."
- If missing info: "What would you like me to [action]?"
"""
```

**Example Agent Behavior**

```python
# User: "Add a task to buy groceries"
# Agent reasoning:
# - Intent: Task creation (keyword "add")
# - Entity: title = "buy groceries"
# - Action: Call add_task

response = add_task(
    user_id="user123",
    title="Buy groceries"
)

agent_response = f"✅ Added task: {response['title']}"

# User: "What's pending?"
# Agent reasoning:
# - Intent: List tasks (keyword "what's")
# - Filter: status = "pending"
# - Action: Call list_tasks

tasks = list_tasks(
    user_id="user123",
    status="pending"
)

agent_response = f"You have {len(tasks)} pending tasks:\n"
for task in tasks:
    agent_response += f"- [{task['id']}] {task['title']}\n"
```

### Common Patterns

**Multi-Turn Clarification**
```
User: "Delete the meeting task"
Agent: (calls list_tasks, finds 3 meetings)
Agent: "I found 3 meeting tasks:
       1. Team meeting
       2. Client meeting
       3. 1-on-1 meeting
       Which one would you like to delete?"
User: "The client one"
Agent: (calls delete_task with task_id=2)
Agent: "✅ Deleted: Client meeting"
```

**Contextual References**
```
User: "Add a task to buy milk"
Agent: "✅ Added task: Buy milk"
User: "Make it high priority"
Agent: (uses context to know "it" = last created task)
Agent: (calls update_task with priority)
Agent: "✅ Updated priority to high for: Buy milk"
```

**Batch Operations**
```
User: "Mark all shopping tasks as complete"
Agent: (calls list_tasks, filters by title containing "shopping")
Agent: (calls complete_task for each)
Agent: "✅ Marked 3 tasks as complete:
       - Buy groceries
       - Get cleaning supplies
       - Purchase birthday gift"
```

### Resources
- OpenAI Agents SDK Documentation
- Natural Language Understanding Patterns
- Conversational UI Best Practices

---