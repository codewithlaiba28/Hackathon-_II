import json
import logging
from typing import AsyncIterator, List, Optional, Any
from datetime import datetime

from chatkit.server import ChatKitServer, StreamingResult, ThreadStreamEvent
from chatkit.store import (
    Store, 
    ThreadMetadata, 
    ThreadItem,
    Page
)
from chatkit.types import UserMessageItem, AssistantMessageItem
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from agents import Agent, Runner

from sqlmodel import Session, select
import models
from src.custom_agents.todo_agent import TodoAgent

logger = logging.getLogger(__name__)

class SQLModelChatKitStore(Store[dict]):
    def __init__(self, engine):
        self.engine = engine

    def _get_session(self):
        return Session(self.engine)

    async def load_thread(self, thread_id: str, context: dict) -> Optional[ThreadMetadata]:
        user_id = context.get("user_id")
        with self._get_session() as session:
            try:
                # thread_id is usually a string from ChatKit, but our DB uses int
                db_id = int(thread_id.replace("thread_", ""))
                conv = session.get(models.Conversation, db_id)
                if conv and (not user_id or conv.user_id == user_id):
                    return ThreadMetadata(id=f"thread_{conv.id}", created_at=int(conv.created_at.timestamp()))
            except:
                pass
        return None

    async def save_thread(self, thread: ThreadMetadata, context: dict):
        user_id = context.get("user_id")
        if not user_id: return
        with self._get_session() as session:
            try:
                db_id = int(thread.id.replace("thread_", ""))
                conv = session.get(models.Conversation, db_id)
                if not conv:
                    conv = models.Conversation(id=db_id, user_id=user_id)
                    session.add(conv)
                    session.commit()
            except:
                pass

    async def load_thread_items(
        self, 
        thread_id: str, 
        after: Optional[str], 
        limit: int, 
        order: str, 
        context: dict
    ) -> Page[ThreadItem]:
        with self._get_session() as session:
            try:
                db_id = int(thread_id.replace("thread_", ""))
                query = select(models.Message).where(models.Message.conversation_id == db_id)
                if order == "desc":
                    query = query.order_by(models.Message.created_at.desc())
                else:
                    query = query.order_by(models.Message.created_at.asc())
                
                messages = session.exec(query).all()
                items = []
                for m in messages:
                    if m.role == "user":
                        items.append(UserMessageItem(
                            id=f"msg_{m.id}",
                            content=[{"type": "text", "text": {"value": m.content}}],
                            created_at=int(m.created_at.timestamp())
                        ))
                    else:
                        items.append(AssistantMessageItem(
                            id=f"msg_{m.id}",
                            content=[{"type": "text", "text": {"value": m.content}}],
                            created_at=int(m.created_at.timestamp())
                        ))
                return Page(data=items, has_more=False)
            except:
                return Page(data=[], has_more=False)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: dict):
        user_id = context.get("user_id")
        if not user_id: return
        with self._get_session() as session:
            try:
                db_id = int(thread_id.replace("thread_", ""))
                if hasattr(item, "role"): # Simple check for message-like items
                    # Get text content
                    text = ""
                    if hasattr(item, "content") and isinstance(item.content, list):
                        for part in item.content:
                            if part.get("type") == "text":
                                text = part["text"]["value"]
                    
                    msg = models.Message(
                        conversation_id=db_id,
                        user_id=user_id,
                        role="user" if item.role == "user" else "assistant",
                        content=text
                    )
                    session.add(msg)
                    session.commit()
            except:
                pass

    def generate_thread_id(self, context: dict) -> str:
        user_id = context.get("user_id")
        with self._get_session() as session:
            conv = models.Conversation(user_id=user_id)
            session.add(conv)
            session.commit()
            session.refresh(conv)
            return f"thread_{conv.id}"

    # --- New required abstract methods in ChatKit 1.5.3 ---
    
    async def load_threads(self, context: dict, limit: int, after: Optional[str] = None, **kwargs) -> Page[ThreadMetadata]:
        user_id = context.get("user_id")
        with self._get_session() as session:
            query = select(models.Conversation).where(models.Conversation.user_id == user_id).order_by(models.Conversation.updated_at.desc())
            conversations = session.exec(query).all()
            threads = [ThreadMetadata(id=f"thread_{c.id}", created_at=int(c.created_at.timestamp())) for c in conversations]
            return Page(data=threads, has_more=False)

    async def delete_thread(self, thread_id: str, context: dict):
        pass

    async def delete_thread_item(self, thread_id: str, item_id: str, context: dict):
        pass

    async def load_item(self, thread_id: str, item_id: str, context: dict) -> Optional[ThreadItem]:
        return None

    async def save_item(self, thread_id: str, item: ThreadItem, context: dict):
        await self.add_thread_item(thread_id, item, context)

    async def load_attachment(self, attachment_id: str, context: dict) -> Any:
        return None

    async def save_attachment(self, attachment_id: str, attachment: Any, context: dict):
        pass

    async def delete_attachment(self, attachment_id: str, context: dict):
        pass

class TodoChatKitServer(ChatKitServer[dict]):
    def __init__(self, store: SQLModelChatKitStore, db_url: str):
        super().__init__(store=store)
        self.db_url = db_url

    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict,
    ) -> AsyncIterator[ThreadStreamEvent]:
        logger.info(f"DEBUG: respond called for thread {thread.id}, user {context.get('user_id')}")
        user_id = context.get("user_id")
        if not user_id:
            logger.error("DEBUG: No user_id in context for respond")
            return

        # 1. Initialize TodoAgent
        import os
        from src.custom_agents.todo_agent import TodoAgent
        todo_agent = TodoAgent(user_id=user_id, db_url=self.db_url)
        
        # Paths for MCP
        # backend/src/chatkit_integration.py -> backend/src -> backend -> phase-III
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        mcp_src_dir = os.path.join(root_dir, "mcp-servers", "todo-tools", "src")
        mcp_script_path = os.path.join(mcp_src_dir, "main.py")

        # 2. Get history from store
        items_page = await self.store.load_thread_items(
            thread.id, after=None, limit=20, order="asc", context=context
        )
        input_items = await simple_to_agent_input(items_page.data)

        # 3. Stream the run
        try:
            async with await todo_agent.get_mcp_server(mcp_script_path, mcp_src_dir) as server:
                agent = await todo_agent.get_agent(server)
                agent_context = AgentContext(thread=thread, store=self.store, request_context=context)
                print("DEBUG: Starting Runner.run_streamed...")
                result = Runner.run_streamed(agent, input_items, context=agent_context)
                print(f"DEBUG: Runner returned result: {result}")
                async for event in stream_agent_response(agent_context, result):
                    print(f"DEBUG: Yielding event: {event}")
                    yield event
                print("DEBUG: Streaming execution completed.")
        except Exception as e:
            logger.error(f"DEBUG: Error in respond streaming: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            print(f"DEBUG: Exception during streaming: {e}")
            raise e
