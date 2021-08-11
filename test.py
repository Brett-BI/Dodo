import redis

import json
import time

#from Connection import ConnectionManager
from Resources import ChannelManager, EventManager

r = redis.Redis()

# def printer(**kwargs): 
#     print('got a message...')
#     print(kwargs['msg'])
#     _r = redis.Redis()
#     _s = _r.pubsub()
#     _s.punsubscribe(kwargs['msg']['data'])

cm = ChannelManager(r)
em = EventManager(r)
cm.create_channel()
time.sleep(5)
cm.create_channel()
time.sleep(5)
cm.create_channel()
time.sleep(5)
cm.create_channel()
time.sleep(5)
# print(cm.create_new_channel())
# cm.add_message({ 'content': 'whats up?', 'sent_at': 'another time'}, 'channel:353957')
# print(cm.messages('channel:353957'))

# def expiry_handler(msg):
#     print("handler: ", msg)
#     print(msg['data'].decode('utf-8'))
#     r.delete('channel:123456')

# ps = r.pubsub()
# ps.psubscribe(**{'__keyevent@0__:expired': expiry_handler})
# ps.run_in_thread(sleep_time=0.1)
# print('doing other stuff...')
#while True:
    
    # for m in ps.listen():
    #     print(m)
