from pydantic import BaseModel

class ChannelRequest(BaseModel):
    pass

class ChannelResponse(BaseModel):
    channel_id: str
    ttl: int