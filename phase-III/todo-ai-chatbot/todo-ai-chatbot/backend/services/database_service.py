from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, and_
from models.task import Task
from models.conversation import Conversation
from models.message import Message
from models.user import User


class DatabaseService:
    """Service for database operations using SQLModel"""

    @staticmethod
    def create_user(session: Session, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return session.exec(select(User).where(User.id == user_id)).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def create_task(session: Session, task_data: Dict[str, Any]) -> Task:
        """Create a new task"""
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID for a specific user"""
        return session.exec(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        ).first()

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get all tasks for a user, optionally filtered by status"""
        query = select(Task).where(Task.user_id == user_id)

        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)
        elif status == "all":
            pass  # Get all tasks regardless of completion status

        return session.exec(query).all()

    @staticmethod
    def update_task(session: Session, task_id: str, user_id: str, update_data: Dict[str, Any]) -> Optional[Task]:
        """Update a task for a specific user"""
        task = session.exec(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        ).first()

        if task:
            for key, value in update_data.items():
                setattr(task, key, value)
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
        return None

    @staticmethod
    def delete_task(session: Session, task_id: str, user_id: str) -> bool:
        """Delete a task for a specific user"""
        task = session.exec(
            select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        ).first()

        if task:
            session.delete(task)
            session.commit()
            return True
        return False

    @staticmethod
    def create_conversation(session: Session, conversation_data: Dict[str, Any]) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(**conversation_data)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation_by_id(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """Get conversation by ID for a specific user"""
        return session.exec(
            select(Conversation).where(
                and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
        ).first()

    @staticmethod
    def create_message(session: Session, message_data: Dict[str, Any]) -> Message:
        """Create a new message"""
        message = Message(**message_data)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message