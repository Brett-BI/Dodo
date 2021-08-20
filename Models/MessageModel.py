from pydantic import BaseModel

class Message(BaseModel):
    content: str
    time_sent: str
    user: str

class MessageResponse(BaseModel):
    messages: list = []
    ttl: int

class MessageRequest(BaseModel):
    content: str
    user: str