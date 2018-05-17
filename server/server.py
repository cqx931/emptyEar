#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
# sudo python server.py
import bottle

app = application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host = '192.168.204.150', port = 80)