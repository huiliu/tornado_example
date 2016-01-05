# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import subprocess
from tornado import gen
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
import time

def test():
    time.sleep(10)
    return "hello"

class GenAsyncHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        #http_client = AsyncHTTPClient()
        #response = yield http_client.fetch("http://www.baidu.com")
        response = yield test()
        self.write(str(response))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        out = runcmd()
        self.write(out)
        

def make_app():
    return tornado.web.Application([
        (r"/", GenAsyncHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
