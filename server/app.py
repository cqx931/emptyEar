#!/usr/bin/env python3
#RUN!
#sudo python server.py

# Reference: https: //github.com/mattmakai/python-websockets-example

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import request, Response
import json

# Subject to change according to network
# ipconfig getifaddr en1
# admin: ve06dd

IP_ADRESS = '192.168.0.21'
PORT = 8080

class toReadList():
    def __init__(self):
        self.dict = {
            "English": [],
            "Danish": [],
            "International": []
        }

    def append(self, item):
        if item.language == "da-DK":
            self.dict["Danish"].append(item)
        elif "en" in item.language:
            self.dict["English"].append(item)
        else :
            self.dict["International"].append(item)
        return;

    def read(self, category):
        message = None
        d = self.dict
        if category == "English" and len(d["English"]) > 1:
            message = d["English"][0]
            d["English"] = d["English"][1: ]# remove the entry
        elif category == "Danish" and len(d["Danish"]) > 1:
            message = d["Danish"][0]
            d["Danish"] = d["Danish"][1: ]# remove the entry
        elif category == "International" and len(d["International"]) > 1:
            message = d["International"][0]
            d["International"] = d["International"][1: ]
            print("Read", category, message)# remove the entry
            return message;
    def clear(self):
        self.dict = {
            "English": [],
            "Danish": [],
            "International": []
            }
        return

    def totalSize(self):
        print(len(self.dict["English"]), len(self.dict["Danish"]), len(self.dict["International"]))
        return len(self.dict["English"]) + len(self.dict["Danish"]) + len(self.dict["International"])


class sttResult(object):
    text = ""
    language = ""
# The class "constructor" - It 's actually an initializer 
    def __init__(self, text, language):
        self.text = text
        self.language = language

#################
# Global variables

_toRead = toReadList()# the set of text to be read
signUpSheet = {
    "main": False,
    "sub-Danish": False,
    "sub-English": False,
    "sub-International": False,
    "count": 0
}
# Future: replace _toRead with db
# db = redis.StrictRedis(IP_ADRESS, PORT, 0)
app = Flask(__name__)
socketio = SocketIO(app)

#################
# Visual
@ app.route("/")
def interface():
    return render_template('main.html')

#########
# socketio
@ socketio.on('connect')
def ws_conn():
    socketio.emit('msg', "connect")

@ socketio.on('disconnect')
def ws_conn():
    socketio.emit('msg', "disconnect")

################
# Start Listening/Reading till all audio clients are online
@ app.route('/hello', methods = ['GET'])# get
def hello_handler(name):
    if signUpSheet[name] == false:
        signUpSheet[name] = True
        signUpSheet[count] += 1

    if ignUpSheet[count] == 4:
        return true
    else:
        return false

#########################
# Listen
# From mainEar.py -> server -> socket
@ app.route('/listen', methods = ['GET'])# get
def listen_handler(name):
    # Push to socket
    socketio.emit('msg', {
        "action": "Listen"
    })
    return

# Read from the server
# subEar.py -> server -> socket
@ app.route('/API/<name>', methods = ['GET'])# get
def read_handler(name):
    '''Handles reads'''
    # Define empty response
    emptyListResponse = Response(json.dumps({
        'text': None,
        'language': None
    }))
    emptyListResponse.headers['Content-Type'] = 'application/json'
    
    category = name[:-1]
    try:
        readed = _toRead.read(category)
    except ValueError: 
    #None if the list is empty
        return emptyListResponse
    
    if not hasattr(readed, 'text'):
        return emptyListResponse

    print('[READ]', readed.text, readed.language, _toRead.totalSize())
    resp = Response(json.dumps({
        'text': readed.text,
        'language': readed.language
    }))
    resp.headers['Content-Type'] = 'application/json'#
    # Push to socket
    socketio.emit('msg', {
        "action": "Read",
        "reader": name,
        "text": readed.text,
        "language": readed.language
    })
    return resp

# Write to the server
@ app.route('/API', methods = ['POST']) # post
def creation_handler():
    try: 
        #parse input data
        try:
            data = json.loads(request.data)# raw format
        except(TypeError, KeyError):
            raise ValueError

        if data is None:
            raise ValueError

        # convert to sttResult
        entry = sttResult(data['text'], data['language'])

    except ValueError: #if bad request data,
        # return 400 Bad Request# here
        Response.status = 400
        return

    except KeyError:
        Response.status = 409
        return

    # add entry
    _toRead.append(entry)

    print('[WRITTEN]', entry.text, entry.language, _toRead.totalSize())# return 200 Success

    resp = Response(json.dumps({
        'text': entry.text
    }))
    resp.headers['Content-Type'] = 'application/json'
    return resp

#@ app.get('/websocket', apply = [websocket])# def echo(ws): #while True: #msg = ws.receive()# if msg is not None: #ws.send(msg)#else :break

#########################

if __name__ == '__main__':
    socketio.run(app, IP_ADRESS, port = PORT, debug = True)

#########################