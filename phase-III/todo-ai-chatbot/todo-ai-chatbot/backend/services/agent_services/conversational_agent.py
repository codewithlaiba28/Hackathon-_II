"""
Conversational Agent (Router)
Role: The primary interface for user interaction. It understands user intent and routes
complex requests to specialized agents or handles simple chitchat directly.
"""
from typing import Dict, Any, List
import re


class ConversationalAgent:
    """
    Conversational Agent (Router)
    Role: The primary interface for user interaction. It understands user intent and routes
    complex requests to specialized agents or handles simple chitchat directly.

    Responsibility:
    - Synthesize user messages.
    - Determine if the request is a "Task Operation" or "General Conversation".
    - Route to Task Planner Agent if tool use is likely needed.
    - Maintain conversational flow and persona.

    Skills: classify_intent, handle_chitchat
    """

    def __init__(self):
        pass

    def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Skill: Classify Intent
        Description: Determines if the user wants to manage tasks or just chat.
        Input Schema: {"message": "string"}
        Output Schema: {"intent": "TASK_MGMT" | "CHITCHAT" | "QUERY"}
        Trigger: On every new user message.
        """
        message_lower = message.lower().strip()

        # Define patterns for task management
        task_patterns = [
            r'\b(add|create|make|new)\b.*\b(task|todo|to-do)\b',
            r'\b(list|show|what|display)\b.*\b(task|todo|to-do)\b',
            r'\b(complete|finish|done|mark)\b.*\b(task|todo|to-do)\b',
            r'\b(delete|remove|erase)\b.*\b(task|todo|to-do)\b',
            r'\b(update|change|modify|edit)\b.*\b(task|todo|to-do)\b',
            r'\b(task|todo|to-do)\b',
            r'\b(buy|get|do|go|call|email|write|read|watch|listen)\b',
        ]

        # Define patterns for chitchat
        chitchat_patterns = [
            r'\b(hi|hello|hey|good morning|good evening|good afternoon)\b',
            r'\b(how are you|how do you do|what\'s up|what\'s new)\b',
            r'\b(who are you|what are you|tell me about yourself)\b',
            r'\b(thanks|thank you|appreciate|grateful)\b',
            r'\b(ok|okay|sure|sounds good|got it)\b',
        ]

        # Check for task management intent
        for pattern in task_patterns:
            if re.search(pattern, message_lower):
                return {"intent": "TASK_MGMT"}

        # Check for chitchat intent
        for pattern in chitchat_patterns:
            if re.search(pattern, message_lower):
                return {"intent": "CHITCHAT"}

        # Default to query if it looks like a question
        if message.strip().endswith('?') or any(q_word in message_lower for q_word in ['what', 'how', 'when', 'where', 'why', 'who']):
            return {"intent": "QUERY"}

        # Default to task management if no clear intent found
        return {"intent": "TASK_MGMT"}

    def handle_chitchat(self, message: str) -> str:
        """
        Skill: Handle Chitchat
        Responds to general conversation with appropriate responses.
        """
        message_lower = message.lower().strip()

        if any(greeting in message_lower for greeting in ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon']):
            return "Hello! I'm your AI assistant for managing todos. You can ask me to add tasks, list your tasks, mark tasks as complete, and more."

        elif any(q in message_lower for q in ['how are you', 'how do you do', 'what\'s up', 'what\'s new']):
            return "I'm doing well, thank you for asking! I'm here to help you manage your tasks and todos. What would you like to do today?"

        elif any(q in message_lower for q in ['who are you', 'what are you', 'tell me about yourself']):
            return "I'm an AI assistant designed to help you manage your tasks and todos. I can create, list, update, and manage your tasks based on your requests."

        elif any(thanks in message_lower for thanks in ['thanks', 'thank you', 'appreciate', 'grateful']):
            return "You're welcome! Is there anything else I can help you with?"

        else:
            return "I'm here to help you manage your tasks. You can ask me to add a task, list your tasks, mark tasks as complete, or delete tasks."

    def process_message(self, message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a user message and determine the appropriate response or routing.
        """
        if history is None:
            history = []

        # Classify the intent of the message
        intent_result = self.classify_intent(message)
        intent = intent_result["intent"]

        if intent == "CHITCHAT":
            # Handle chitchat directly
            response = self.handle_chitchat(message)
            return {
                "response_type": "direct_response",
                "response": response,
                "needs_task_planning": False
            }
        elif intent in ["TASK_MGMT", "QUERY"]:
            # Route to Task Planner Agent
            return {
                "response_type": "route_to_planner",
                "user_message": message,
                "intent": intent,
                "needs_task_planning": True
            }
        else:
            # Default to task planning
            return {
                "response_type": "route_to_planner",
                "user_message": message,
                "intent": "TASK_MGMT",
                "needs_task_planning": True
            }