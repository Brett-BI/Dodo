from enum import Enum
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import redis

from Models import ChannelModel, MessageModel
from Resources import ChannelManager, EventManager, ChannelNotFoundError


app = FastAPI()
r = redis.Redis()

cm = ChannelManager(r)
#em = EventManager(r)

# TODO Create response models for channel and message operations or something (makes outgoing responses uniform?)
# TODO Connect requests to endpoints to methods in the ChannelManager
# TODO WebSockets...
# TODO Create request models (makes incoming requests uniform?)
# TODO KeyEvent notification system
# TODO Add logic to verify that the user requesting data is actually part of the channel before anything is returned. Not sure how to do this...
# TODO Add logic to automatically parse through/json_dumps the Redis stuff

# global error handling
@app.exception_handler(ChannelNotFoundError)
async def channel_not_found_exception_handler(request, exc):
    return JSONResponse({'message': exc.message}, status_code=404)

@app.get('/')
async def root():
    return "this is the root."

@app.post('/channel/new', response_model=ChannelModel.ChannelResponse, status_code=201)
async def create_channel():
    new_channel = cm.create_channel(r)
    return new_channel

@app.get('/channel/{channel_id}/messages')
async def get_messages(channel_id: str):
    pass
    # might want to consider chunking later, if it looks necessary

@app.post('/channel/{channel_id}/messages/add', response_model=MessageModel.MessageResponse, status_code=201)
async def add_message(channel_id: str, req: MessageModel.MessageRequest):
    if cm.check_channel_exists() == False:
        raise HTTPException(status_code=404, detail="Channel not found.")

    cm.add_message(req, channel_id)
    _messages = cm.get_messages(channel_id)
    _ttl = cm.get_ttl(channel_id)
    return MessageModel.MessageResponse(messages=_messages, ttl=_ttl)
        

@app.get('/channel/{channel_id}/ttl')
async def get_ttl(channel_id: str):
    pass

@app.get('/channel/{channel_id}', response_model=ChannelModel.Channel, status_code=200)
async def get_channel(channel_id: str):
    # print(cm.check_channel_exists(channel_id))
    # if cm.check_channel_exists(channel_id) == False:
    #     raise ChannelNotFoundError()
        
    return cm.get_channel_data(channel_id) 
    # return all of the data for a channel (ChannelModel.Channel + list of messages?)


