from typing import List, Dict

# In-memory stores
session_store: List[Dict] = [
    {
        "session_id": 1,
        "session_user": "abc",
        "created_at": "2025-06-30T16:00:00"
    }
]

chat_store: Dict[int, List[Dict[str, str]]] = {
    1: [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ]
}
