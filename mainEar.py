#!/usr/bin/env python3

# Put this in /Library/WebServer/Documents/
# sudo python server.py
# Hit Ctrl-C to quit.

from bottle import route, Bottle, run

# general library
import json
import time
import sys
# Call tts script
from subprocess import call
# obtain path to "english.wav" in the same folder as this script
from os import path
# Threading
from threading import Thread
# main library: Speech recognition
import speech_recognition as sr

# Settings
dbug = True
LAN_LIMIT = 10

# Files
GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(open("data/googleCloudCred.json", 'r')))
LANGUAGE_CODE_FILE = "data/languageCode.txt"
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "data/title.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")

# Default
LANGUAGES = []
TARGET = LANGUAGES
ENGLISHES = []
DANISH = ["da-DK","da-DK","da-DK","da-DK","da-DK","da-DK"]
OTHERS = []
EARS = [ENGLISHES, DANISH, OTHERS]

# Main functions
######################################
# Overwrite the Recognizer class

class MySR(sr.Recognizer):
    def __init__(self):
        sr.Recognizer.__init__(self)
        self.energy_threshold = 200

######################################
class sttResult(object):
    text = ""
    language = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, text, language):
        self.text = text
        self.language = language

class toReadList():
    def __init__(self):
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
     	return message;


def loadLanguages():
  with open(LANGUAGE_CODE_FILE , 'r') as myfile:
    data = myfile.read()
    languages = data.split('\n')
    for s in languages:
        s = s[0:s.find(',')]
        LANGUAGES.append(s)
        if "en" in s:
            ENGLISHES.append(s)
        else:
            OTHERS.append(s)
  return;

def recSphinx(audio):
    # recognize speech using Sphinx
    try:
        result = r.recognize_sphinx(audio)
        pt("Sphinx thinks you said " + result)
        return result;
    except sr.UnknownValueError:
        pt("Sphinx could not understand audio")
        return "";
    except sr.RequestError as e:
        pt("Sphinx error; {0}".format(e))
        return "";

def recGoogleTest(audio):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        pt("Google Speech Recognition thinks you said " + result)
        return result;
    except sr.UnknownValueError:
        pt("Google Speech Recognition could not understand audio")
        return "";
    except sr.RequestError as e:
        pt("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "";

def recGoogleCloud(audio, lg, results=None):
    # Recognize speech using Google Cloud Speech
    # Supported languages: https://cloud.google.com/speech-to-text/docs/languages
    global toRead

    try:
        result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language=lg)
        pt("Google Cloud Speech thinks you said " + result)
        
        item = sttResult(result, lg)
        toRead.append(item)
        return result;
    except sr.UnknownValueError:
        pt("Google Cloud Speech could not understand audio " + lg)
        if "en" in lg :
            # If it is English, Try sphinx 
            pt("Try Sphinx")
            return recSphinx(audio)
        else:
            return "";
    except sr.RequestError as e:
        pt("Could not request results from Google Cloud Speech service; {0}".format(e))
        return "";

def batchRequestGoogleCloud(audio, target, limit):
    # TODO
    
    subArray = target[0:limit+1]
    threads = [None] * len(subArray)
    idx = 0

    for lg in subArray:
        threads[idx] = Thread(target=recGoogleCloud, args=(audio, lg))
        threads[idx].start()
        idx = idx + 1

    # do some other stuff
    for i in range(len(threads)):
        threads[i].join()
    
    return;

def getTTSLanguageCode(code):
    if "Han" in code:
        code = "zh_" + code[-2:]
    else:
        code = code.replace("-", "_")
    return code;

def speechRecHandler(recognizer, audio):
    # TODO: Tell the subEars to stop reading???
    pt("Audio detected, processing...")
    T_recognition = Thread(target=recog,args=(audio,TARGET))
    T_recognition.start()
    return

def printAllLanguageCode():
    pt("Supported languages:")
    for lg in LANGUAGES:
        pt(lg + " " + getTTSLanguageCode(lg));
    return

def pt(message):
    if dbug: print(message);

def recog(audio, target):
    pt("*********THREAD_RECOGNIZING*********")
    results = batchRequestGoogleCloud(audio, target, LAN_LIMIT)
    return

def startServer():
    run(app, host='192.168.204.150', port=80)
    return
#######################

#SEVER
app = Bottle()
# Define the responses
@app.route('/Hello')
def getDanish():
    return 'Hello!'
@app.route('/Danish')
def getDanish():
    return toRead.read("Danish")
@app.route('/English')
def getEnglish():
    message = toRead.read("English")
    return message
@app.route('/International')
def getInternational():
    return toRead.read("International")

T_server = Thread(target=startServer)
T_server.start()

#######################

print("...initializing...")
# Initialize speech recognition
r = MySR()

# Load language list
loadLanguages()
pt("Speech recognition with " + str(len(LANGUAGES)) + " Languages")

# Load the sample audio file
with sr.AudioFile(AUDIO_FILE) as source:
    sampleAudio = r.record(source)  

# shared Global variables
toRead = toReadList()

T_recognition = Thread(target=recog,args=(sampleAudio,TARGET))
T_recognition.start()

pt("Welcome to the empty ear machine! Say something!")
# Start listening
# obtain audio from the microphone
m = sr.Microphone()

# listen for 1 second and create the ambient noise energy level
with m as source:
    r.adjust_for_ambient_noise(source, duration=1)

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, speechRecHandler) 


