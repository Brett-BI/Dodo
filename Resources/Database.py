import redis

from abc import abstractmethod
import json
from random import randint
from typing import Dict, List

# Interface for the Room, Message, and User classes. Need the initialize method for initial setup of the object in Redis.
class DatabaseObject():
    @abstractmethod
    def initialize(self) -> None:
        pass

# ignoring users for now
class User(DatabaseObject):
    pass
    '''
        {
            id: alphanumeric
            create_time: datetime
            pub/sub: pub/sub data
        }
    '''


class Message(DatabaseObject):
    def __init__(self, redis_instance: redis.Redis, channel_id: str) -> None:
        self.r = redis_instance
        self.channel_id = channel_id

    # there's never going to be a need to init the entire class here because this is only ever called in the Channel class...
    def initialize(self) -> None:
        self.r.hset(self.channel_id, 'messages', json.dumps([]))

    def add_message(self, message: Dict) -> None:
        self.messages.append(message)    





'''
    ? Should we use a generic Database class that can then be implemented by Users, Rooms, and Messages?
    ? Should we use generic classes for Users, Rooms, and Messages that assume you're passing in a Redis db object?
        > This means we would need another class for initializing the DB setup OR overseeing the setup using Users, Rooms, and Messages so:
          Ex.: DBOverseer().init([databaseclasses])
          ! Need to make a separate interface for Users, Rooms, and Messages that guarantees the presence of an init() method for DBOverseer.init() to call on each database object
    ! Users -> Channels.channel_id.messages
      Should look like this: channels = { ch:1234: { messages: [], users: [], start_time: [] }}
                             users = { user:1234: { created_date: "" }}
'''