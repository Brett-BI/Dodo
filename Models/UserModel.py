from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    time_created: str

class UserResponse(BaseModel):
    user_id: str

