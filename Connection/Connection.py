import fastapi

class Connection():
    def __init__(self, channel_id: str, websocket: fastapi.WebSocket) -> None:
        self.channel_id = channel_id
        self.websocket = websocket