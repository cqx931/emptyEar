#!/usr/bin/env python3
from bottle import request, response
from bottle import post, get, put, delete

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
        if category == "English":
            message = self.dict["English"][0]
            toRead.English[1:] # remove the entry
        elif category == "Danish":
            message = self.dict["Danish"][0]
            toRead.Danish[1:]
        else:
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

@post('/handler')
def creation_handler():
    try:
        # parse input data
        try:
            data = request.json()
        except:
            raise ValueError

        if data is None:
            raise ValueError

        # extract and validate name
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
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add name
    _toRead.append(entry)
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'text': entry.text})

@get('/handler')
def listing_handler():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps(_toRead.dict)

@put('/handler/<name>')
def read_handler(name):
    '''Handles reads'''
    try:
        if _toRead.totalSize() == 0:
            raise EmptyError
    except EmptyError:
        response.status = 404
        return "The List is empty"

    # if not
    return json.dumps(_toRead.read(name))
    