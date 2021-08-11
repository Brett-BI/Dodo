from abc import abstractmethod

# Interface for the Room, Message, and User classes. Need the initialize method for initial setup of the object in Redis.
class RedisResource():
    @abstractmethod
    def initialize(self) -> None:
        pass

class EmitResource():
    @abstractmethod
    def initialize(self) -> None:
        pass