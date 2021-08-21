class ChannelNotFoundError(Exception):
    def __init__(self, message="Channel not found.") -> None:
        self.message = message
    
    def __str__(self):
        return f'{self.message}'

