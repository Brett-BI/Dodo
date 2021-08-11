from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import redis

import json

from ConnectionManager import ConnectionManager

app = FastAPI()
r = redis.Redis()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket(`ws://localhost:8000/ws${window.location.pathname}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                console.log(event.data);
                console.log(event);
                message.appendChild(content)
                messages.appendChild(message)
                console.log('Listening...');
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/{channel_id}")
async def get():
    return HTMLResponse(html)

'''
    ! This is going to require a new way of organizing the data. We're going to need a datastructure for managing the client IDs and the channels they're in so that
      we can broadcast to a specific channel for the user to be updated instead of sending out a broadcast to all users for all channels every time something is
      updated... Might be tricky. This seems like the best solution for the time being though - managing a list of connections and broadcasting to a filtered subset
      of them as needed.
    ! Need to develop a cleaner mechanism for broadcasting updates to a specific channel.
'''

manager = ConnectionManager()

# use query param for the channel id, form data for the messages... 
@app.websocket("/ws/{channel_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id):
    #await websocket.accept()
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(channel_id)
        print(data)
        _channels_data = json.loads(r.get('channels'))
        print(_channels_data)
        if channel_id in _channels_data:
            #_channel_data = _channels_data[channel_id]
            _channels_data[channel_id]['messages'].append(data)
            r.set('channels', json.dumps(_channels_data))
        else:
            _channels_data[channel_id] = {'messages': [data]}
            r.set('channels', json.dumps(_channels_data))
        
        #await websocket.send_json(_channels_data[channel_id])
        await manager.broadcast(_channels_data[channel_id])
        #_messages = json.loads(r.get('messages'))
        #print(_messages)
        #updated_messages = _messages[:]
        #updated_messages.append(data)
        #r.set('messages', json.dumps(updated_messages))
        #await websocket.send_json(updated_messages)