"""
Task Planner Agent (Orchestrator)
Role: Breaks down high-level user goals into specific executable steps.
"""
from typing import Dict, Any, List
import re


class TaskPlannerAgent:
    """
    Task Planner Agent (Orchestrator)
    Role: Breaks down high-level user goals into specific executable steps.

    Responsibility:
    - Analyze "Task Operation" intents.
    - Map intents to specific MCP Tool calls.
    - Identify missing parameters and ask clarifying questions (via the Conversation Agent, or directly if architecture permits return-to-user).
    - Formulate a plan of tool executions.

    Skills: extract_task_parameters, plan_tool_sequence
    """

    def __init__(self):
        pass

    def extract_task_parameters(self, user_request: str) -> Dict[str, Any]:
        """
        Skill: Extract Task Parameters
        Extract relevant parameters from a user request.
        """
        # Initialize parameters
        params = {
            "description": None,
            "task_id": None,
            "status": None,
            "due_date": None,
            "priority": None,
            "limit": None
        }

        # Extract description for add_task
        add_patterns = [
            r"(?:add|create|make|new)\s+(?:task|to|for)?\s*(.+?)(?:\s+(?:and|with|using|by|before|due)\b|$)",
            r"(?:add|create|make|new)\s+(.+?)(?:\s+(?:and|with|using|by|before|due)\b|$)"
        ]

        for pattern in add_patterns:
            match = re.search(pattern, user_request, re.IGNORECASE)
            if match:
                description = match.group(1).strip()
                if description.lower() not in ['task', 'a task', 'the task', 'an task']:
                    params["description"] = description
                    break

        # Extract task ID if mentioned
        task_id_match = re.search(r'(?:task|id)\s*(\d+)', user_request, re.IGNORECASE)
        if task_id_match:
            params["task_id"] = task_id_match.group(1)

        # Extract status if mentioned
        if 'complete' in user_request.lower() or 'done' in user_request.lower() or 'finished' in user_request.lower():
            params["status"] = "completed"
        elif 'pending' in user_request.lower() or 'incomplete' in user_request.lower() or 'not done' in user_request.lower():
            params["status"] = "pending"

        # Extract priority if mentioned
        if 'high priority' in user_request.lower() or 'urgent' in user_request.lower() or 'asap' in user_request.lower():
            params["priority"] = "high"
        elif 'low priority' in user_request.lower() or 'not urgent' in user_request.lower():
            params["priority"] = "low"
        elif 'medium priority' in user_request.lower():
            params["priority"] = "medium"

        # Extract limit if mentioned
        limit_match = re.search(r'(?:limit|show|display|up to|at most)\s+(\d+)\s+(?:tasks|items|results)', user_request, re.IGNORECASE)
        if limit_match:
            try:
                params["limit"] = int(limit_match.group(1))
            except ValueError:
                pass

        return params

    def plan_tool_sequence(self, user_request: str) -> Dict[str, Any]:
        """
        Skill: Plan Tool Sequence
        Converts a natural language request into a sequence of tool calls.

        Input Schema: {"request": "buy milk and delete the old gym task"}
        Output Schema:
        {
          "steps": [
            {"tool": "add_task", "args": {"description": "buy milk"}},
            {"tool": "delete_task", "args": {"search_term": "gym"}}
          ]
        }
        Failure Case: Ambiguous request -> Returns encoded "Ask Clarification".
        """
        user_request_lower = user_request.lower()
        steps = []

        # Handle multiple operations in a single request
        # Split the request by conjunctions like "and", "then", etc.
        sub_requests = re.split(r'\s+(?:and|then|after|followed by|next)\s+', user_request)

        for sub_request in sub_requests:
            sub_request = sub_request.strip()
            if not sub_request:
                continue

            # Determine which tool to use based on the sub-request
            if any(word in sub_request for word in ['add', 'create', 'make', 'new']):
                # Extract parameters for add_task
                params = self.extract_task_parameters(sub_request)
                if params["description"]:
                    steps.append({
                        "tool": "add_task",
                        "args": {
                            "description": params["description"],
                            "priority": params["priority"] or "medium"
                        }
                    })

            elif any(word in sub_request for word in ['list', 'show', 'what', 'display', 'view']):
                # Extract parameters for list_tasks
                status = None
                if 'completed' in sub_request or 'done' in sub_request:
                    status = "completed"
                elif 'pending' in sub_request or 'incomplete' in sub_request or 'not done' in sub_request:
                    status = "pending"
                elif 'all' in sub_request:
                    status = "all"

                args = {}
                if status:
                    args["status"] = status
                if params.get("limit"):
                    args["limit"] = params["limit"]

                steps.append({
                    "tool": "list_tasks",
                    "args": args
                })

            elif any(word in sub_request for word in ['complete', 'finish', 'done', 'mark']):
                # Extract parameters for complete_task
                params = self.extract_task_parameters(sub_request)
                if params["task_id"]:
                    steps.append({
                        "tool": "complete_task",
                        "args": {
                            "task_id": params["task_id"]
                        }
                    })
                else:
                    # If no specific task ID, we might need to list tasks first to identify the right one
                    # For now, return an error indicating the need for clarification
                    return {
                        "is_ambiguous": True,
                        "missing_info": "Which specific task would you like to mark as complete?",
                        "steps": []
                    }

            elif any(word in sub_request for word in ['delete', 'remove', 'erase']):
                # Extract parameters for delete_task
                params = self.extract_task_parameters(sub_request)
                if params["task_id"]:
                    steps.append({
                        "tool": "delete_task",
                        "args": {
                            "task_id": params["task_id"]
                        }
                    })
                else:
                    # If no specific task ID, we might need to list tasks first to identify the right one
                    return {
                        "is_ambiguous": True,
                        "missing_info": "Which specific task would you like to delete?",
                        "steps": []
                    }

            elif any(word in sub_request for word in ['update', 'change', 'modify', 'edit']):
                # Extract parameters for update_task
                params = self.extract_task_parameters(sub_request)
                if params["task_id"]:
                    update_args = {"task_id": params["task_id"]}
                    if params["description"]:
                        update_args["description"] = params["description"]
                    if params["status"]:
                        update_args["status"] = params["status"]

                    steps.append({
                        "tool": "update_task",
                        "args": update_args
                    })
                else:
                    # If no specific task ID, return an error indicating the need for clarification
                    return {
                        "is_ambiguous": True,
                        "missing_info": "Which specific task would you like to update?",
                        "steps": []
                    }

        return {
            "is_ambiguous": False,
            "missing_info": None,
            "steps": steps
        }

    def analyze(self, user_request: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Analyze a user request and create a plan of action.
        """
        if history is None:
            history = []

        # Plan the tool sequence based on the user request
        plan = self.plan_tool_sequence(user_request)

        return plan