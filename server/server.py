#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
# sudo python server.py
from bottle import Bottle, run
from bottle import request, response
import json

# Subject to change according to network
# ipconfig getifaddr en1
# library 192.168.204.150
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
        message = ""
        if category == "English" and len(self.dict["English"]) > 1:
            message = self.dict["English"][0]
            toRead.English[1:] # remove the entry
        elif category == "Danish" and len(self.dict["Danish"]) > 1:
            message = self.dict["Danish"][0]
            toRead.Danish[1:]
        elif len(self.dict["International"]) > 1:
            message = self.dict["International"][0]
            toRead.International[1:]
        print("Read", category, message)
        return message
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
    	print(name)
        #if _toRead.totalSize() == 0:
            #raise EmptyError
    except EmptyError:
        response.status = 404
        return "The List is empty"
    # if not
    return json.dumps(_toRead.read(name))

#

@app.post('/API')
def creation_handler():
    try:
        # parse input data      
        try:  	
            data = request.json()
            print(data)
        except:
            raise ValueError

        if data is None:
            raise ValueError

        # extract and validate 
        try:
            entry = sttResult()
            entry.text = data['text']
            entry.language = data['language']
        except (TypeError, KeyError):
            raise ValueError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return

    except KeyError:
        response.status = 409
        return

    # add entry
    _toRead.append(entry)
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'text': entry.text})

run(app, host=IP_ADRESS, port=80)

# copy the file to server folder
# cp /Users/admin/emptyEar/server/server.py /Library/WebServer/Documents/