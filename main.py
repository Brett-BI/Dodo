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

@app.post('/channel/{channel_id}/messages/add', response_model=MessageModel.MessageResponse, status_code=201)
async def add_message(channel_id: str, req: MessageModel.MessageRequest):
    print(channel_id)
    cm.add_message(req, channel_id)
    _messages = cm.messages(channel_id)
    return MessageModel.MessageResponse(messages=_messages['messages'], ttl=_messages['ttl'])

# can also have channel/about, channel/ttl, channel/{id}/messages/delete, channel/{id}/messages/get?chunk=10&page=2

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# @app.get('/')
# async def root():
#     return {'messages', 'hi'}

@app.post("/items/")
async def read_items(item: Item, q: Optional[str] = Query(None, max_length=50)):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get('/items1/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}

class ItemTypes(str, Enum):
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'

@app.get('/itemNames/{item_name}')
async def get_items(item_name: ItemTypes):
    if item_name == ItemTypes.alexnet:
        return {'item_type': item_name, 'message': 'Deep Learning something or other...'}
    
    if item_name == ItemTypes.lenet:
        return {'item_type': item_name, 'message': 'LeCNN all images. Blast off.'}
    
    return {'item_type': item_name, 'message': 'Some other item type.'}


# Query params - anything that isn't part of the path.
fake_items_db = [
    {'item_name': 'foo'},
    {'item_name': 'bar'},
    {'item_name': 'baz'}
]

@app.get('/items2/')
async def read_item(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    return fake_items_db[skip : skip + limit]