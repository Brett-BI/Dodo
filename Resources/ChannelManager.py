import redis

import json
from random import randint
from datetime import timedelta
from typing import Callable, Dict, List

from .Resource import RedisResource
from .EventManager import EventManager

class ChannelManager(RedisResource):
    def __init__(self, redis_instance: redis.Redis) -> None:
        self.r = redis_instance

    # error handling...
    def create_channel(self, emit_callable: Callable = None) -> str:
        channel_id = 'channel:' + str(round(randint(100000, 999999))) # "namespace"
        
        if self.r.get(channel_id) == None:
            #_channels = json.loads(self.r.get('channels'))
            #_channels.append({ channel_id: { 'messages': [], 'created_at': 'sometime'}})
            self.r.set(channel_id, json.dumps({ 'messages': [], 'created_at': 'sometime'})) # copying the entire list feels bad...
            self.r.expire(channel_id, timedelta(seconds=20)) # can change to something else later...
            #em = EventManager(self.r, channel_id, emit_callable) # create a new instance of the EventManager for this? Will this even run?
            print(f'{channel_id} set to expire in 60 seconds...')
            return channel_id
        else:
            self.create_channel()        
    
    # throw a proper error...
    def add_message(self, message: Dict, channel_id: str) -> None:
        if self.r.get(channel_id):
            #_messages = self.messages(channel_id)
            _channel = json.loads(self.r.get(channel_id))
            _channel['messages'].append(message)
            self.r.set(channel_id, json.dumps(_channel))            
        else:
            print('channel does not exist, son.') 
 
    def messages(self, channel_id: str) -> List:
        return json.loads(self.r.get(channel_id))['messages'] if self.r.get(channel_id) else []
    
    def update_channel_expiration(self, channel_id: str, expiration_time: timedelta = timedelta(seconds=20)) -> None:
        self.r.expire(channel_id, expiration_time)
        print(f'{channel_id} updated to expire in {timedelta} seconds...')