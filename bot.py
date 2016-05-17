#from compile import *

from flask import Flask, request, Response
import json
import requests


import os

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

@app.route("/compile", methods = ['GET', 'POST'])
def interact():
    if request.method == 'GET':
        return {"response" : "OKAY"}
    if request.method == 'POST':
    	return {"response" : "POST OKAY"}

@app.route('/')
def hello():
    return "hello"

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)