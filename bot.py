#from compile import *

from flask import Flask, request, Response, jsonify
import json
import requests


import os

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

@app.route("/compile", methods = ['POST'])
def interact(vlog_url = None):
    if request.method == 'POST':
    	vlog_url = request.args.get('vlog_url', '')
    	j = {'vlog_url' : vlog_url}
    	return jsonify(**j)

@app.route('/')
def hello():
    return "hello"

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)