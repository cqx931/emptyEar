#!/usr/bin/env python3
import sys
import pyttsx3
import random
import http.client, subprocess
import json
# httplib for python2, http.client for python3

voiceDict = {}
mode = "International"
if len(sys.argv) > 1:
    mode = sys.argv[1]
# python subEar English
# python subEar Dannish
# python subEar International

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

def defaultRead():
    # TODO: read sentence and language from data
    # if no answer received, read emptyMachine
    print("default Read")
    return

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

# Change IP here
c = http.client.HTTPConnection('192.168.0.21', 80)

while True:
    c.request('GET', '/API/' + mode)
    try:
        data = c.getresponse().read()
    except ValueError:
        print("No response")
    try:
        data = json.loads(data.decode())
    except ValueError:
        print("Unable to process data")
    if data == None:
      defaultRead()
    else: 
      sentence = data["text"]
      language = data["language"]
      print("Received:", sentence,language)
      language = getTTSLanguageCode(language)
      voice = randomVoice(language)
      say(sentence)