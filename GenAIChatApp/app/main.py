from fastapi import FastAPI
from app.src.routes import session_router

app = FastAPI(title="GenAI Chat App")

app.include_router(session_router, tags=["session"])
