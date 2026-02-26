from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import StreamingResponse
from db import engine, DATABASE_URL
import auth
import models

router = APIRouter()

@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user)
):
    from src.chatkit_integration import SQLModelChatKitStore, TodoChatKitServer
    from chatkit.server import StreamingResult
    store = SQLModelChatKitStore(engine)
    server = TodoChatKitServer(store, DATABASE_URL)
    
    # Pass user_id in context
    context = {"user_id": current_user.id}
    
    try:
        # Process request
        print(f"DEBUG: ChatKit endpoint received request from user {context.get('user_id')}", flush=True)
        body = await request.body()
        print("DEBUG: Request body received, processing with server...", flush=True)
        result = await server.process(body, context)
        print("DEBUG: Server process completed.", flush=True)
        
        if isinstance(result, StreamingResult):
            return StreamingResponse(
                result, 
                media_type="text/event-stream",
                headers={"X-Accel-Buffering": "no"}
            )
        
        return Response(content=result.json, media_type="application/json")
    except Exception as e:
        import traceback
        print("CRITICAL ERROR in chatkit_endpoint:")
        traceback.print_exc()
        return Response(content=str(e), status_code=500)
