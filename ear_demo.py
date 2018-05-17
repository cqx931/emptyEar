#!/usr/bin/env python3


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
LAN_LIMIT = 9

# Files
GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(open("data/googleCloudCred.json", 'r')))
LANGUAGE_CODE_FILE = "data/languageCode.txt"
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "data/title.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")

# Default
LANGUAGES = []
# Three ears for the click festival
ENGLISHES = []
DANISH = ["da-DK","da-DK","da-DK","da-DK","da-DK","da-DK"]
OTHERS = []
EARS = [ENGLISHES, DANISH, OTHERS]

# Set Target
if len(sys.argv) == 1:
    TARGET = LANGUAGES
else:
    TARGET = EARS[int(sys.argv[1]) - 1]

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
    
    if len(toRead) > 0:
        T_read = Thread(target=readFromPool)
        T_read.start() # Start Reading!
    return;

def getTTSLanguageCode(code):
    if "Han" in code:
        code = "zh_" + code[-2:]
    else:
        code = code.replace("-", "_")
    return code;

def speechRecHandler(recognizer, audio):
    global T_recognition
    if T_read.isAlive():
            T_read.join()
            toRead = []
    if T_recognition.isAlive():
            T_recognition.join()
    pt("Audio detected, processing...")
    T_recognition = Thread(target=recog,args=(audio,TARGET))
    T_recognition.start()
    return;

def printAllLanguageCode():
    pt("Supported languages:")
    for lg in LANGUAGES:
        pt(lg + " " + getTTSLanguageCode(lg));
    return;

def pt(message):
    if dbug: print(message);

######################################
# MAIN TREADS #

def readFromPool():
    pt("*********THREAD_READING*********")
    global toRead
    while len(toRead) > 0:
      e = toRead[0]
      # pt("[READ]" + e.text)
      call(["python3", "tts.py", e.text, getTTSLanguageCode(e.language)])
      toRead = toRead[1:] # remove the entry
    return;

def recog(audio, target):
    pt("*********THREAD_RECOGNIZING*********")
    results = batchRequestGoogleCloud(audio, target, LAN_LIMIT)
    return;

######################################
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
toRead = []

#Threading
# 1.Listening is always on in the background
# 2.Batch recognition is fired when audio is detected
# 3.Reading thread is fired, after getting the first result from a batch recognition process

T_read = Thread(target=readFromPool)
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
# `stop_listening` is now a function that, when called, stops background listening

# calling this function requests that the background listener stop listening
# stop_listening(wait_for_stop=False)
# do some more unrelated things
while True: 
    # print("@ " + str(r.is_Recording) + " " + str(r.energy_threshold))
    # if r.is_Recording : 
    #     pt("Listening...")
    #     # terminate other threads if alive & clear the list
       
    time.sleep(1)

 # do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# do some more unrelated things
while True: time.sleep(0.1)
#