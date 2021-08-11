import redis
import json

r = redis.Redis()

def pub():
    data = {
        'message': 'hi',
        'from': 'me',
        'to': 'you'
    }

    r.publish('broadcast', json.dumps(data))

if __name__ == "__main__":
    pub()