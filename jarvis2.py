import speech_recognition as sr
from time import ctime
import time
import threading
import cv2
import sys
import logging as log
import datetime as dt
import os
import pyjokes
import wikipedia
import requests
from pygame import mixer
from gtts import gTTS

mixer.init()
os.system("jack_control start")
os.system("arecord -l")

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    print("SAVED")
    #os.system("mpg321 audio.mp3")
    mixer.music.load('audio.mp3')
    mixer.music.play()
    

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(sr.Microphone())
        print(sr.Recognizer())
        print("Say something!")
        audio = r.listen(source)
        print("Heard")
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data

def weather():
  def weather_data(query):
    res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=8de0c1d186a15c6c44a58c73ca31e976&units=metric');
    return res.json();
  def print_weather(result,city):
    w1 = ("{}'s temperature: {}°C ".format(city,result['main']['temp']))
    w2 = ("Wind speed: {} meters per second".format(result['wind']['speed']))
    w3 = ("Weather description: {}".format(result['weather'][0]['description']))
    w = w1 + w2 + w3 

    print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
    print("Wind speed: {} m/s".format(result['wind']['speed']))
    print("Description: {}".format(result['weather'][0]['description']))
    print("Weather: {}".format(result['weather'][0]['main']))
    speak(w)
  def main():
    city="Toronto"
    print()
    try:
      query='q='+city;
      w_data=weather_data(query);
      print_weather(w_data, city)
      print()
    except:
      print('City name not found...')

  if __name__=='__main__':
    main()


def jarvis(data):

    if "tell me a joke" in data:
        joke = pyjokes.get_joke()
        speak(joke)

    if "tell me the weather" in data:
        weather()

    if "how are you" in data:
        speak("I am fine")

    if "what time is it" in data:
        speak(ctime())

    if "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Mr.Tahbahtah, I will show you where " + location + " is.")
        os.system("start https://www.google.nl/maps/place/" + location + "/&amp;")

    if "look up" in data:
        try:
            data = data.split(" ")
            query = data[2]
            speak("Hold on Mr.Tahbahtah, I'll look up " + query)
            wiki_res = wikipedia.summary(query, sentences=2)
            speak(wiki_res)
        except wikipedia.exceptions.PageError:
            print("An error occured, coudn't find anything on: " + query)
            speak("An error occured, coudn't find anything on: " + query)
        
        except requests.exceptions.ConnectionError:
            print("A connection error occured, coudn't find anything on: " + query)
            speak("A connection error occured, coudn't find anything on: " + query)



# initialization
time.sleep(2)
speak("Hello Mr.Tahbahtah, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)
