#!/usr/bin/env python3

# Network related
from bottle import route, Bottle, run
import requests
import httplib, urllib

# General library
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
LAN_LIMIT = 20
IP_ADDRESS = '192.168.0.20'
PORT = '8080'
POSTURL = 'http://' + IP_ADDRESS + ':' + PORT + '/API'

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
    # recognize speech using Sphinx: in case internet is not working
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
        
        item = {
            "text": result,
            "language": lg
        }
        toRead.append(item)
        # Broadcast to server
        headers = {'Content-type': 'application/json'}
        requests.post(POSTURL, data=json.dumps(item), headers=headers)
        quit()
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
    # TODO: Sequence
    
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
    
    # deal with the other half
    subArray = target[limit:]

    
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

#######################

print("...initializing...")
# Initialize speech recognition
r = MySR()
# Initialize server
# Change Server IP
c = httplib.HTTPConnection(IP_ADDRESS, 80)
c.request('GET', '/')
data = c.getresponse().read()
print(data)

# Load language list
loadLanguages()
pt("Speech recognition with " + str(len(LANGUAGES)) + " Languages")

# Load the sample audio file
with sr.AudioFile(AUDIO_FILE) as source:
    sampleAudio = r.record(source)  

# shared Global variables
toRead = []

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

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# do some more unrelated things
while True: time.sleep(0.1)
#
