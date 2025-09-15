from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timezone
from typing import Optional, List

from app.src.schemas import CreateSessionRequest, CreateSessionResponse, Message
from app.src.models import session_store, chat_store

session_router = APIRouter(prefix="/sessions")


@session_router.post("", response_model=CreateSessionResponse)
def create_session(payload: CreateSessionRequest):
    session_user = payload.session_user.strip().lower()
    session_id = len(session_store) + 1
    created_at = datetime.now(timezone.utc).isoformat()

    new_session = {
        "session_id": session_id,
        "session_user": session_user,
        "created_at": created_at
    }

    session_store.append(new_session)
    chat_store[session_id] = []

    return new_session


@session_router.post("/{session_id}/messages")
def add_message(session_id: int, message: Message):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found")

    if message.role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    chat_store[session_id].append({
        "role": message.role,
        "content": message.content
    })

    return {"message": "Message added successfully"}


@session_router.get("/{session_id}/messages", response_model=List[Message])
def get_messages(session_id: int, role: Optional[str] = Query(None)):
    if session_id not in chat_store:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = chat_store[session_id]

    if role:
        if role not in ["user", "assistant"]:
            raise HTTPException(status_code=400, detail="Invalid role filter")
        messages = [msg for msg in messages if msg["role"] == role]

    return messages
