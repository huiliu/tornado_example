# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, render_template, Response, redirect, url_for
from .notifier import WebSocket
import json
from .utils.inventory import PlayBookFactory, async_run_playbook
import threading
import time

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

def long_task():
    time.sleep(5)
    print('long task')
    

@app.route('/run')
def longtask_view():
    pb = PlayBookFactory('production', inventory='op/inventory')
    #pb.run_task()
    async_run_playbook(pb)

    t = threading.Thread(target=long_task)
    t.start()
    
    return redirect(url_for('index_view'))
    return make_response(Response())
