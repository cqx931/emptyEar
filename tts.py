
SAVE_TO_FILE= True;

import sys
import pyttsx3
import random

def init_engine():
    engine = pyttsx3.init()
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
    return;

print("init")
engine = init_engine()
print("tts", sys.argv[1],sys.argv[2])
voice = randomVoice(str(sys.argv[2]))
say(str(sys.argv[1]))
# TODO: Save to file