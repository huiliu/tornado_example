# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, render_template, Response
from .notifier import WebSocket
import json

app = Flask(__name__)

@app.route('/api/<path:version>/<path:action>', methods=['POST'])
def api_view(version, action):
    """
    """
    data = request.form
    print(data)
    WebSocket.send_message(json.dumps(data))
    return make_response(Response())

@app.route('/')
def index_view():
    return render_template('index.html')
