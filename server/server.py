#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
    return "Welcome to the Empty Ear Machine!"
@app.route('/')
def connect():
    return "Connected!"
run(app, host='192.168.204.150', port=80)
