#!/usr/bin/env python3

# main library
import speech_recognition as sr
import pyttsx3

# general library
import json
import random

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "speech_recognition/examples/french.aiff")
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# Main functions
######################################
def changeSpeechSpeed(rate):
    # default 200, range 50,300
    engine.setProperty('rate', rate);
    return;

def printAllVoices():
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.id)
    return;

def randomVoice(lan):
    # set a random voice
    while True:
        randomVoice = random.choice(voices);
        if (lan in randomVoice.languages[0]):
            print(randomVoice)
            break
    engine.setProperty('voice', randomVoice.id);

def recSphinx(audio):
    # recognize speech using Sphinx
    try:
        result = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + result)
        engine.say(result)
        return result;
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return "";
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return "";

def recGoogleTest(audio):
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + result)
        return result;
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "";
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "";

def recGoogleCloud(audio):
    # # recognize speech using Google Cloud Speech
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = json.dumps(json.load(open("googleCloudCred.json", 'r')))
    try:
        result = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        engine.say(result)
        print("Google Cloud Speech thinks you said " + result)
        return result;
    except sr.UnknownValueError:
        print("Google Cloud Speech could not understand audio")
        return "";
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))
        return "";

######################################
# Main
# init Text to Speech Engine
engine = pyttsx3.init()

print("Welcome to the empty ear machine! Say something!")
print("press x to quite")
# printAllVoices()
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
#print("Please wait. Calibrating microphone...")
# listen for 1 second and create the ambient noise energy level
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source,phrase_time_limit=5)

# # use the audio file as the audio source
# # r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#     audio = r.record(source)  # read the entire audio file


#
# # speech to text
result = recGoogleTest(audio)
# randomVoice("en")
# specify voice setting
engine.setProperty('rate', 150);
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Zarvox');

# text to speech
if (result != ""):
  engine.say(result)

engine.runAndWait()
