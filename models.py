from pydantic import BaseModel

class Conversation(BaseModel):
    user_id: str
    conversation_id: str
    message: str
    response: str
