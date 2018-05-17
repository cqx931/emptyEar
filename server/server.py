#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
# sudo python server.py
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

# Subject to change according to network
# ipconfig getifaddr en1
# library 192.168.204.150
run(app, host='192.168.0.21', port=80)

# copy the file to server folder
# cp /Users/admin/emptyEar/server/server.py /Library/WebServer/Documents/