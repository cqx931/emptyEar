#!/usr/bin/env python3
from bottle import request, response
from bottle import post, get, put, delete

class toReadList():
    def __init__(self):
        self.dict = 
        self.English = []
        self.Danish = []
        self.International = []
    def append(self, item):
        if item.language == "da-DK":
            self.Danish.append(item)
        elif "en" in item.language:
            self.English.append(item)
        else:
            self.International.append(item)
    def read(self, category):
        message = ""
        if category == "English":
            message = self.English[0]
            toRead.English[1:] # remove the entry
        elif category == "Danish":
            message = self.Danish[0]
            toRead.Danish[1:]
        else:
            message = self.International[0]
            toRead.International[1:]
        print("Read", category, message)
        return message

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
    return json.dumps({'names': list(_names)})

@put('/handler/<name>')
def update_handler(name):
    '''Handles name updates'''
    pass

@delete('/handler/<name>')
def delete_handler(name):
    '''Handles name deletions'''
    pass
