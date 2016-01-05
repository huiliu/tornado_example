
from tornado.websocket import WebSocketHandler

class WebSocket(WebSocketHandler):
    """
    """
    clients = set()
    def open(self, *args):
        self.clients.add(self)
        print("Socket open!")

    def on_message(self, message):
        self.write_message("Received:" + message)

    def on_close(self):
        if self in self.clients:
            self.clients.remove(self)
        print("Socket Closed!")

    @classmethod
    def send_message(cls, message):
        for c in cls.clients:
            print(message)
            c.write_message(message)
