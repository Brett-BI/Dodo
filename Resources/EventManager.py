import redis

import threading
from typing import Callable, Dict

class EventManager():
    # handlers is going to a dict of handler methods (need to be subclassed) if we want to specify different handlers for each event type (EXPIRE, SET, etc.)
    def __init__(self, redis_instance: redis.Redis, handlers: Dict = None) -> None:
        self.r = redis_instance
        self.handlers = handlers
        self._setup_subscription()
        
    def _setup_subscription(self) -> None:
        subscription = self.r.pubsub()        
        # subscribe to all EXPIRE events for now in a separate thread and leave it open.
        subscription.psubscribe(**{'__keyevent@0__:expired': self.notification_handler})
        subscription.run_in_thread(sleep_time=0.1)
        
    def emit_handler(self, thread: threading.Thread) -> None:
        self.emit_callable()
        thread.close()
    
    # probably a good idea to sub-class this so that multiple parsers/notification handlers can be implemented...
    def notification_handler(self, message: Dict) -> None:
        print(message)
        # TODO send notification to websocket manager to push to front end.