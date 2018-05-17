#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
from bottle import run
import bottle

app = application = bottle.default_app()

run(app, host='192.168.204.150', port=80)