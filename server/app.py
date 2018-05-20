#!/usr/bin/env python3
#RUN!
#sudo python server.py

# Reference: https: //github.com/mattmakai/python-websockets-example

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import request, Response
import json
from random import randint
import random
# Subject to change according to network
# ipconfig getifaddr en1
# admin: ve06dd

IP_ADRESS = '92.168.160.109'
PORT = 8080
DEFAULT_RESULT_FILE = 'data/testResult.txt'

class toReadList():
    def __init__(self):
        self.dict = {
            "English": [],
            "Danish": [],
            "International": []
        }
        self.defaultDictionary = loadDefaultResult()

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

        if self.totalSize() == 0:
            self.getFromDefault()
          
        if category == "english" and len(d["English"]) > 0:
            # return random English
            message = d["English"][randint(0, len(d["English"]))]
        elif category == "danish" and len(d["Danish"]) > 0:
            message = d["Danish"][0]
        elif category == "international" and len(d["International"]) > 0:
            message = d["International"][randint(0, len(d["International"]))]
            d["International"] = d["International"][1: ]# remove the entry
        #control the reading thread
        ## END IF ###

        print("[Read]", category, message,category == "international", self.intlSize(), self.totalSize() )
        
        return message;

    def clear(self):
        self.dict = {
            "English": [],
            "Danish": [],
            "International": []
            }
        return

    def getFromDefault(self):
        item = self.getRandomFromDefault("Danish")
        self.append(item)

        for i in range(0, 2):
            item = self.getRandomFromDefault("English")
            self.append(item)
        for i in range(0, 6):
            item = self.getRandomFromDefault("International")
            self.append(item)

    def getRandomFromDefault(self, lg):
        return random.choice(self.defaultDictionary[lg])

    def intlSize(self):
        return len(self.dict["International"])

    def totalSize(self):
        return len(self.dict["International"]) + len(self.dict["Danish"]) + len(self.dict["English"])

class sttResult(object):
    text = ""
    language = ""
# The class "constructor" - It 's actually an initializer 
    def __init__(self, text, language):
        self.text = text
        self.language = language


def loadDefaultResult():
    size = 0
    d = {
            "English": [],
            "Danish": [],
            "International": []
    }
    with open(DEFAULT_RESULT_FILE , 'r') as myfile:
        data = myfile.read()
        lines = data.split('\n')
        for s in lines:
            size += 1
            parts = s.split(':')
            lg = parts[0]
            text = parts[1]
            item = sttResult(text,lg)

            if lg == "da-DK":
                d["Danish"].append(item)
            elif "en" in lg:
                d["English"].append(item)
            else :
                d["International"].append(item)
    
    print("Loaded default result:", size, len(d["Danish"]), len(d["English"]), len(d["International"]))
    return d

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
def listen_handler():
    # Push to socket
    socketio.emit('msg', {
        "action": "Listen"
    })
    print('[LISTEN]')
    # clear the list
    _toRead.clear()

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
    
    # Due with category and name
    category = name.lower()
    category = category[:-1]

    if category.startswith("international"):
        category = "international"


    try:
        readed = _toRead.read(category)
    except ValueError: 
    #None if the list is empty
        return emptyListResponse
    
    if not hasattr(readed, 'text'):
        return emptyListResponse
    
    # Push to socket -> Display first
    socketio.emit('msg', {
        "action": "Read",
        "reader": name,
        "text": readed.text,
        "language": readed.language
    })

    print('[READ]', readed.text, readed.language, _toRead.intlSize())
    resp = Response(json.dumps({
        'text': readed.text,
        'language': readed.language
    }))
    resp.headers['Content-Type'] = 'application/json'#

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

    print('[WRITTEN]', entry.text, entry.language, _toRead.intlSize())# return 200 Success

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