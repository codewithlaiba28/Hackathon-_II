from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import StreamingResponse
from chatkit.server import StreamingResult
from db import engine, DATABASE_URL
from src.chatkit_integration import SQLModelChatKitStore, TodoChatKitServer
import auth
import models

router = APIRouter()
store = SQLModelChatKitStore(engine)
server = TodoChatKitServer(store, DATABASE_URL)

@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user)
):
    # Pass user_id in context
    context = {"user_id": current_user.id}
    
    try:
        # Process request
        print(f"DEBUG: ChatKit endpoint received request from user {context.get('user_id')}")
        body = await request.body()
        print("DEBUG: Request body received, processing with server...")
        result = await server.process(body, context)
        print("DEBUG: Server process completed.")
        
        if isinstance(result, StreamingResult):
            return StreamingResponse(result, media_type="text/event-stream")
        
        return Response(content=result.json, media_type="application/json")
    except Exception as e:
        import traceback
        print("CRITICAL ERROR in chatkit_endpoint:")
        traceback.print_exc()
        return Response(content=str(e), status_code=500)
