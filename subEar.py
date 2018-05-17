#!/usr/bin/env python3
import sys
import pyttsx
import random
import httplib, subprocess

def init_engine():
    engine = pyttsx.init()
    return engine

def say(s):
    engine.say(s)
    engine.runAndWait() #blocks

def randomVoice(lan):
    # set a random voice
    voices = engine.getProperty('voices')
    while True:
        randomVoice = random.choice(voices);
        if (lan in randomVoice.languages[0]):
            # print(randomVoice)
            break
    if randomVoice.id: engine.setProperty('voice', randomVoice.id);

def changeSpeechSpeed(rate):
    # default 200, range 0,400
    return

def defaultRead():
    # TODO: read sentence and language from data
    # if no answer received, read emptyMachine
	return

print("init tts")
engine = init_engine()
c = httplib.HTTPConnection('192.168.204.150', 80)
c.request('GET', '/Hello')
data = c.getresponse().read()
print(data)

# while loop
c.request('GET', '/API', 'English')
data = c.getresponse().read()
print(data)

if data == None:
	defaultRead()
else:	
	sentence = data.text
	language = data.langauge
	print("tts", sentence,language)
	voice = randomVoice(str(language))
	say(sentence)