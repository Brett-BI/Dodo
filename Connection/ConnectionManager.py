from fastapi import WebSocket

from typing import List

from Connection import Connection

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str, channel_id: str):
        for connection in self.active_connections:
            await connection.send_json(message)

        
# NOTE: doing it this way instead of using Redis Pub/Sub seems easier. Unsure of how channels are really setup in Redis but there's also the issue
# of emitting the events for each of those channels. Seems easier to just manage the broadcast to specific users here.
# ! Need to use redis' pubsub to setup a pub/sub relationship between FastAPI and Redis. THEN, use FastAPI WebSocket to emit those events to the front end...
#   ? How the f*** to set this up - pub/sub and websockets. The WebSocket is going to have to maintain the pub/sub? One connection with pub/sub and broadcast to clients?

# TODO:
# - Build a connection object comprised of at least 2 parts: the channel_id for the connection and a list of websocket objects. (allows broadcast to be sent to all websockets
#   associated with a single "connection".)
# - Build a method that manages the addition of new websockets (does this also have to manage the expiration of websockets too when the channel expires?)