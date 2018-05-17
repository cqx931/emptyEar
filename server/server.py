#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
from bottle import Bottle, run
from bottle import request, response

app = Bottle()

@app.route('/hello')
def hello():
    return "Welcome to the Empty Ear Machine!"
@app.route('/')
def connect():
    return "Connected!"
@app.get('/API')
def listing_handler():
    #response.headers['Content-Type'] = 'application/json'
    #esponse.headers['Cache-Control'] = 'no-cache'
    return "test"

#TODO: API should goes here
run(app, host='192.168.204.150', port=80)
