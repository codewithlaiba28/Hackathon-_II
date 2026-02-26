from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate
from ..models.message import Message, MessageCreate
from uuid import UUID
from datetime import datetime


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation_create: ConversationCreate, user_id: UUID) -> Conversation:
        """
        Create a new conversation for a user
        """
        conversation = Conversation(
            title=conversation_create.title,
            is_active=conversation_create.is_active,
            user_id=user_id
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_user_conversations(self, user_id: UUID) -> List[Conversation]:
        """
        Get all conversations for a user
        """
        conversations = self.session.exec(
            select(Conversation).where(Conversation.user_id == user_id)
        ).all()
        return conversations

    def get_conversation_by_id(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a user (ensures user owns the conversation)
        """
        conversation = self.session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
        ).first()
        return conversation

    def update_conversation(self, conversation_id: UUID, conversation_update: ConversationUpdate, user_id: UUID) -> Optional[Conversation]:
        """
        Update a conversation for a user
        """
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            return None
            
        update_data = conversation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(conversation, field):
                setattr(conversation, field, value)
                
        conversation.updated_at = datetime.now()
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def delete_conversation(self, conversation_id: UUID, user_id: UUID) -> bool:
        """
        Delete a conversation for a user
        """
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        if not conversation:
            return False
            
        self.session.delete(conversation)
        self.session.commit()
        return True

    def add_message_to_conversation(self, conversation_id: UUID, message_create: MessageCreate) -> Optional[Message]:
        """
        Add a message to a conversation
        """
        # Verify that the conversation exists and belongs to the user
        conversation = self.session.exec(
            select(Conversation).where(Conversation.id == conversation_id)
        ).first()
        
        if not conversation:
            return None
            
        message = Message(
            conversation_id=message_create.conversation_id,
            sender_type=message_create.sender_type,
            content=message_create.content,
            metadata=message_create.metadata
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_conversation_messages(self, conversation_id: UUID, user_id: UUID) -> List[Message]:
        """
        Get all messages for a conversation (ensures user owns the conversation)
        """
        messages = self.session.exec(
            select(Message)
            .join(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
            .order_by(Message.timestamp)
        ).all()
        return messages
