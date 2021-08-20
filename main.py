from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel
import redis

from Models import ChannelModel, MessageModel
from Resources import ChannelManager, EventManager


app = FastAPI()
r = redis.Redis()

cm = ChannelManager(r)
#em = EventManager(r)

# TODO Create response models for channel and message operations or something (makes outgoing responses uniform?)
# TODO Connect requests to endpoints to methods in the ChannelManager
# TODO WebSockets...
# TODO Create request models (makes incoming requests uniform?)
# TODO KeyEvent notification system

@app.get('/')
async def root():
    return "this is the root."

@app.post('/channel/new', response_model=ChannelModel.ChannelResponse, status_code=201)
async def create_channel():
    new_channel = cm.create_channel(r)
    return new_channel

@app.get('/channel/{channel_id}/messages')
def get_messages(channel_id: str):
    pass
    # might want to consider chunking later, if it looks necessary

@app.post('/channel/{channel_id}/messages/add', response_model=MessageModel.MessageResponse, status_code=201)
async def add_message(channel_id: str, req: MessageModel.MessageRequest):
    print(channel_id)
    cm.add_message(req, channel_id)
    _messages = cm.get_messages(channel_id)
    return MessageModel.MessageResponse(messages=_messages['messages'], ttl=_messages['ttl'])

@app.post('/channel/{channel_id}/ttl')
def get_ttl(channel_id: str):
    pass

@app.post('/channel/{channel_id}', response_model=ChannelModel.Channel, status_code=200)
def get_channel(channel_id: str):
    return cm.get_channel_data(channel_id) 
    # return all of the data for a channel (ChannelModel.Channel + list of messages?)


