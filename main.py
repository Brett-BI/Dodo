from enum import Enum
from typing import Optional
import time

from fastapi import FastAPI, Query, HTTPException, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis

from Models import ChannelModel, MessageModel, UserModel
from Resources import ChannelManager, EventManager, UserManager, ChannelNotFoundError


app = FastAPI()
r = redis.Redis()

cm = ChannelManager(r)
um = UserManager(r)
#em = EventManager(r)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.exception_handler(redis.ConnectionError)
async def redis_connection_error_handler(request, exc):
    return JSONResponse({'message': 'Redis instance could not be reached.'}, status_code=500)


@app.post('/test/{id}')
def test(id: str):
    return {'message': id}


@app.get('/channel/new', response_model=ChannelModel.Channel, status_code=201)
async def create_channel():
    new_channel = cm.create_channel()
    time.sleep(5)
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


@app.get('/user/create', response_model=UserModel.User, status_code=201)
async def create_user():
    new_user = um.create_user()
    time.sleep(5)    
    return new_user


@app.websocket('/socket')
async def socket(websocket: WebSocket): # wtf is the point of passing in the websocket?
    print('connection..?')
    await websocket.accept()
    await websocket.send_json({'status': 'connected'})
    while True:
        time.sleep(3)
        await websocket.send_json({'tick': 'tock'})

# need to build out the ConnectionManager so that it can handle all connections
# endpoint also needs be channel specific, probably (but how to manage that from the ConnectionManager?)
# ? Should a random ID be assigned to a a connection?
# ? How to close a connection? 
# ? When to close a connection?
# ConnectionManager needs to send messages using some sort of Model (unsure if existing will work or if new will be needed)
# need a lot of error handling for various events that may come up (dropped connection, etc.)
# would be nice to have some information about the websocket so some troubleshooting can be done & mgmt is easier
# need to make the socket endpoint accept messages too
# ? how are websockets secured?