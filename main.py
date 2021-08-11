from enum import Enum
from typing import Optional

from fastapi import FastAPI
import redis

from .database import Database

app = FastAPI()
rds = redis.Redis(db=15)

@app.get('/')
async def root():
    return {'messages', []}

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

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    return fake_items_db[skip : skip + limit]