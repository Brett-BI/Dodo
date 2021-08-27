from json import decoder
import redis

import json
from random import randint
from datetime import timedelta, datetime
from typing import Callable, Dict, List

from .Resource import RedisResource
from .EventManager import EventManager
from Models.UserModel import User

class UserManager(RedisResource):
    def __init__(self, redis_instance: redis.Redis) -> None:
        self.r = redis_instance

    def _redis_check(func: callable) -> None:
        # pings the Redis server before running the function. The ping() will throw a ConnectionError (handled globally by Starlette)
        def wrapper(*args):
            print('Pinging Redis server instance...')
            self = args[0]            
            self.r.ping()
            return func(*args)
            
        return wrapper

    # error handling...
    @_redis_check
    def create_user(self) -> User:
        user_id = 'user:' + str(round(randint(100000, 999999))) # "namespace"
        
        if self.r.get(user_id) == None:
            _user = User(user_id=user_id, time_created=str(datetime.now()))
            self.r.set(user_id, json.dumps(_user.dict()))
            print(f'Created {user_id}...')
            return _user
        else:
            self.create_user()
