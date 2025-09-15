from pydantic import BaseModel, field_validator
from typing import Literal


class CreateSessionRequest(BaseModel):
    session_user: str

    @field_validator("session_user")
    def validate_user(cls, value):
        clean = value.strip().lower()
        if not clean:
            raise ValueError("Username cannot be empty")
        return clean


class CreateSessionResponse(BaseModel):
    session_id: int
    session_user: str
    created_at: str


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str
