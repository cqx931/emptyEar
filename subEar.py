#!/usr/bin/env python3
import requests

import pyttsx3

import sys
import random
import json
import time

voiceDict = {}

IP_ADDRESS = '92.168.160.109'
PORT = '8080'

mode = "internationalA1"
if len(sys.argv) > 1:
    mode = sys.argv[1]

GETURL = 'http://' + IP_ADDRESS + ':' + PORT + '/API/' + mode
# python subEar english1/2/3
# python subEar dannish
# python subEar international

#####################
def init_engine():
    engine = pyttsx3.init()
    return engine

def say(s):
    engine.say(s)
    engine.runAndWait() #blocks

def randomVoice(lan):
    voices = voiceDict[lan]
    while True:
        randomVoice = random.choice(voices);
        print(randomVoice.languages[0])
        if (lan in randomVoice.languages[0]):
            # 
            break
    if randomVoice.id: engine.setProperty('voice', randomVoice.id);

def changeSpeechSpeed(rate):
    # default 200, range 0,400
    return

def getTTSLanguageCode(code):
    if "Han" in code:
        code = "zh_" + code[-2:]
    else:
        code = code.replace("-", "_")
    return code;

def filterVoices():
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.languages[0] not in voiceDict.keys():
            voiceDict[voice.languages[0]] = [voice]
        else: 
            voiceDict[voice.languages[0]].append(voice)
    return
#####################
print("init tts")
engine = init_engine()
filterVoices()


while True:
    r = requests.get(GETURL)
    
    try: 
        data = json.loads(r.content)
        print(data)
        if data["text"] == None and data["language"] == None:

            time.sleep(1) 
        else: 
            sentence = data["text"]
            language = data["language"]
            print("Received:", sentence,language)
            language = getTTSLanguageCode(language)
            voice = randomVoice(language)
            say(sentence)
            time.sleep(1) 
    except:
        ValueError

   