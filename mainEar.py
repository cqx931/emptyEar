#!/usr/bin/env python3

# Network related
import requests

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
LAN_LIMIT = 8
IP_ADDRESS = '192.168.0.20'
PORT = '8080'
POSTURL = 'http://' + IP_ADDRESS + ':' + PORT + '/API'
HELLOURL = 'http://' + IP_ADDRESS + ':' + PORT + '/hello/master'
LISTENURL = 'http://' + IP_ADDRESS + ':' + PORT + '/listen'

# Files
GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(open("data/googleCloudCred.json", 'r')))
LANGUAGE_CODE_FILE = "data/languageCode.txt"
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "data/title.wav")
DEFAULT_AUDIO_FILES = ["data/english.wav"]
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

class BatchGoogleProcess:
    def __init__(self, r, audio, target):
        self.r = r
        self.audio = audio
        self.name = str(int(time.time()))[-6:] #last 6 digit of time stamp
        self.target = target[:LAN_LIMIT]
        self.toRead = []
        self.stopFlag = False

    def start(self):
        for lg in self.target:
            if self.stopFlag: 
                break
            recGoogleCloud(self.r, self, self.audio,lg)

    def stop(self):
        self.stopFlag = True

######################################
class sttResult(object):
    text = ""
    language = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, text, language):
        self.text = text
        self.language = language
SENTINEL = "SENTINEL"


def loadLanguages():
    global LANGUAGES
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

############ KEY #############

def recog(r, audio, target):
    global currentBatch
    # both sampleAudio and audio detected
    pt("*********New Batch Process*********")
    # new batchGoogleProcess
    batchGoogle = BatchGoogleProcess(r, audio, target)
    pt("Batch" + batchGoogle.name)
    batchGoogle.start()
    currentBatch = batchGoogle

def listen(r, m):
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, speechRecHandler) 

def speechRecHandler(recognizer, audio):
    
    pt("*********Audio detected, processing*********")

    # tell server: Listening 
    ready = requests.get(LISTENURL)

    # Stop old batch thread
    if currentBatch is not None:
        currentBatch.stop()
        pt("Stop Batch" + currentBatch.name)
    
    #new recog
    recog(r,audio,TARGET)
    
    # T_recognition = Thread(target=recog,args=(audio,TARGET))
    # T_recognition.start()
    return

##################

def recSphinx(audio): # Not in use
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

def recGoogleTest(audio): # Not in use
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

def recGoogleCloud(r, batchGoogle, audio, lg, results=None):
    # Recognize speech using Google Cloud Speech
    # Supported languages: https://cloud.google.com/speech-to-text/docs/languages
    
    try:
        result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,language=lg)
        pt(batchGoogle.name + "|" + "Google Cloud Speech thinks you said " + result + " " + lg)
        item = {
            "text": result,
            "language": lg
        }
        batchGoogle.toRead.append(item)
        # Broadcast to server
        headers = {'Content-type': 'application/json'}
        requests.post(POSTURL, data=json.dumps(item), headers=headers)
        return result;
    except sr.UnknownValueError:
        pt("Google Cloud Speech could not understand audio " + lg)
        # if "en" in lg :
        #     # If it is English, Try sphinx 
        #     pt("Try Sphinx")
        #     return recSphinx(audio)
        # else:
        return "";
    except sr.RequestError as e:
        pt("Could not request results from Google Cloud Speech service; {0}".format(e))
        return "";

def getTTSLanguageCode(code):
    if "Han" in code:
        code = "zh_" + code[-2:]
    else:
        code = code.replace("-", "_")
    return code;

def printAllLanguageCode():
    pt("Supported languages:")
    for lg in LANGUAGES:
        pt(lg + " " + getTTSLanguageCode(lg));
    return

def pt(message):
    if dbug: print(message);

#######################
 
# global
currentBatch = None
r = MySR()

def my_main_function():
    # Initialize speech recognition
    # Initialize server
    # Change Server IP

    ready = requests.get(HELLOURL)
    data = ready.content

    # while not ready:
    #     ready = requests.get(POSTURL)
    #     time.sleep(3)

    # Load language list
    loadLanguages()
    pt("Speech recognition with " + str(len(LANGUAGES)) + " Languages")

    # Load the sample audio file
    with sr.AudioFile(AUDIO_FILE) as source:
        sampleAudio = r.record(source)  

    #########################################
    
    pt("Welcome to the empty ear machine! Say something!")
    # Start listening
    # obtain audio from the microphone
    m = sr.Microphone()

    # listen for 1 second and create the ambient noise energy level
    with m as source:
        r.adjust_for_ambient_noise(source, duration=1)

    # listening thread
    T_listening = Thread(target=listen, args=(r,m))
    T_listening.start()

    # start with sample
    T_recognition = Thread(target=recog,args=(r, sampleAudio,TARGET))
    T_recognition.start()

    # do some unrelated computations for 5 seconds
    for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

    # do some more unrelated things
    while True: time.sleep(0.1)  #
 
if __name__=='__main__':
    try:
        my_main_function()
    except:
        # restart with keyboard interaction
        my_main_function()



