#!/usr/bin/env python3
#encoding: utf-8
# Put this in the server folder
# cp /Users/admin/emptyEar/server/server.py /Library/WebServer/Documents/
# RUN!
# sudo python server.py



from bottle import Bottle, run
from bottle import request, response
import json
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
# Subject to change according to network
# ipconfig getifaddr en1
# library 192.168.204.150
# ONSITE 05.18, RIGHT SIDE.  192.168.204.139
IP_ADRESS = '192.168.0.21'

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
        else:
            self.dict["International"].append(item)

    def read(self, category):
        message = None
        d = self.dict
        if category == "English" and len(d["English"]) > 1:
            message = d["English"][0]
            d["English"] = d["English"][1:] # remove the entry
        elif category == "Danish" and len(d["Danish"]) > 1:
            message = d["Danish"][0]
            d["Danish"] = d["Danish"][1:] # remove the entry
        elif category == "International" and len(d["International"]) > 1:
            message = d["International"][0]
            d["International"] = d["International"][1:]
        print("Read", category, message) # remove the entry
        return message

    def clear(self):
    	self.dict = {
            "English": [],
            "Danish": [],
            "International": []
        }
        return

    def totalSize(self):
        return len(self.dict["English"]) + len(self.dict["Danish"]) + len(self.dict["International"])


class sttResult(object):
    text = ""
    language = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, text, language):
        self.text = text
        self.language = language

_toRead = toReadList()     # the set of text to be read

app = Bottle()

#################
@app.route('/hello')
def hello():
    return "Welcome to the Empty Ear Machine!"
@app.route('/')
def connect():
    return "Connected to Server!"

#########################
@app.get('/API/<name>')
def read_handler(name):
    '''Handles reads'''
    try:
    	readed = _toRead.read(name)
        #if _toRead.totalSize() == 0:
            #raise EmptyError
    except EmptyError:
    	# None if the list is empty
        response.status = 404
        return "The List is empty"
    # if not
    response.headers['Content-Type'] = 'application/json'
    print('[READ]', readed.text, readed.language, _toRead.totalSize())
    return json.dumps({'text': readed.text,'language':readed.language})

#

@app.post('/API')
def creation_handler():
    try:
        # parse input data      
        try:
            data = json.loads(request.body.read()) #raw format
        except (TypeError, KeyError):
            raise ValueError
        
        if data is None:
        	raise ValueError
        
        # convert to sttResult
        entry = sttResult(data['text'],data['language'])

    except ValueError:
        # if bad request data, return 400 Bad Request
        #here
        response.status = 400
        return

    except KeyError:
        response.status = 409
        return

    # add entry
    _toRead.append(entry)
    print('[WRITTEN]', entry.text, entry.language, _toRead.totalSize())
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'text': entry.text})

@app.get('/websocket', apply=[websocket])
def echo(ws):
    while True:
        msg = ws.receive()
        if msg is not None:
            ws.send(msg)
        else: break
        
#########################

run(app, host=IP_ADRESS, port=8080, server=GeventWebSocketServer)

#########################
