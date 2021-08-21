from json import decoder
import redis

import json
from random import randint
from datetime import timedelta, datetime
from typing import Callable, Dict, List

from .Resource import RedisResource
from Resources.Errors import ChannelNotFoundError
from .EventManager import EventManager
from Models import Channel, ChannelResponse, Message

class ChannelManager(RedisResource):
    def __init__(self, redis_instance: redis.Redis) -> None:
        self.r = redis_instance

    def _redis_check(func: callable) -> None:
        # pings the Redis server before running the function. The ping() will throw a ConnectionError (handled globally by Starlette)
        def wrapper(*args):
            print('Pinging Redis server instance...')
            self = args[0]            
            self.r.ping()
            func(*args)
            
        return wrapper


    @_redis_check
    def _channel_exists(self, channel_id: str) -> bool:
        if self.r.get(channel_id):
            return True
        
        raise ChannelNotFoundError

    @_redis_check
    def get_channel_data(self, channel_id: str) -> Channel:
        if self._channel_exists(channel_id):
            channel = Channel(channel_id=channel_id, ttl= self.get_ttl(channel_id), messages=self.get_messages(channel_id))
            return channel


    # error handling...
    @_redis_check
    def create_channel(self, emit_callable: Callable = None) -> ChannelResponse:
        channel_id = 'channel:' + str(round(randint(100000, 999999))) # "namespace"
        
        if self.r.get(channel_id) == None:
            self.r.set(channel_id, json.dumps({ 'messages': [], 'created_at': 'sometime'})) # copying the entire list feels bad...
            self.r.expire(channel_id, timedelta(seconds=60)) # can change to something else later...
            #em = EventManager(self.r, channel_id, emit_callable) # create a new instance of the EventManager for this? Will this even run?
            print(f'{channel_id} set to expire in 60 seconds...')
            return ChannelResponse(channel_id=channel_id, ttl=120)
        else:
            self.create_channel()


    # throw a proper error...
    # def add_message(self, message: Dict, channel_id: str) -> None:
    #     print(self.r.keys())
    #     print(list(map(lambda k: k.decode('utf-8'), self.r.keys())))
    #     channel_id = "something:1234"
    #     if channel_id in list(map(lambda k: k.decode('utf-8'), self.r.keys())):
    #         _channel = json.loads(self.r.get(channel_id))
    #         print(_channel)
    #         _channel['messages'].append(message.dict())
    #         print(_channel)
    #         self.r.set(channel_id, json.dumps(_channel))  
    #         self.update_channel_expiration(channel_id, timedelta(minutes=1))
    #     else:
    #         raise IndexError()


    @_redis_check
    def add_message(self, message: Dict, channel_id: str) -> None:
        if self._channel_exists(channel_id):
            _channel = json.loads(self.r.get(channel_id))
            print(_channel)
            _channel['messages'].append(message.dict())
            print(_channel)
            self.r.set(channel_id, json.dumps(_channel))  
            self._update_channel_expiration(channel_id, timedelta(minutes=1))


    @_redis_check
    def get_messages(self, channel_id: str) -> List[Message]:
        messages = []
        if self._channel_exists(channel_id):
            _messages = json.loads(self.r.get(channel_id))['messages']
            if len(_messages) > 0:
                for _m in _messages:
                    messages.append(Message(content=_m['content'], user=_m['user'], time_sent=datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        
        return messages

    
    @_redis_check
    def _update_channel_expiration(self, channel_id: str, expiration_time: timedelta = timedelta(minutes=2)) -> None:
        if self._channel_exists(channel_id):
            self.r.expire(channel_id, expiration_time)        
            print(f'{channel_id} updated to expire in {timedelta.seconds} seconds...')


    @_redis_check
    def get_ttl(self, channel_id: str) -> int:
        return self.r.ttl(channel_id)

    
# import the models here and use them. Just return the models and the endpoint logic won't have to do anything else but return the result of the function...