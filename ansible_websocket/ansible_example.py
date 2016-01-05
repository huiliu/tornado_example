
from tornado.ioloop import IOLoop
import tornado.web
import subprocess
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.web import Application, FallbackHandler
from tornado.httpclient import AsyncHTTPClient

from app.flasky import app
from app.notifier import WebSocket

container = WSGIContainer(app)

application = Application([
    (r'/websocket/', WebSocket),
    (r'.*', FallbackHandler, dict(fallback=container))
])

server = HTTPServer(application)
server.bind(8080)
server.start(0)

IOLoop.current().start()
