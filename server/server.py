#!Python
# Put this in /Library/WebServer/Documents/
from bottle import route, Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
	return 'Hello World!'

run(app, host='192.168.204.150', port=80)