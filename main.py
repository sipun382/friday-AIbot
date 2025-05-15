import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import os
import wikipedia
import requests
import subprocess
import time
import musicl  # Your existing music module
import json
import random
#import openai  # AI Chat Integration

# Initialize recognizer & text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def get_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")

def get_weather(city="Your City"):
    api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        temp = response["main"]["temp"]
        description = response["weather"]["description"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't retrieve the weather information.")

def get_news():
    api_key = "your_news_api_key"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    articles = response["articles"][:5]
    news_list = [article["title"] for article in articles]
    speak("Here are the top news headlines:")
    for news in news_list:
        speak(news)

def play_song(song_name):
    if song_name in musicl.music:
        webbrowser.open(musicl.music[song_name])
        speak(f"Playing {song_name} on your preferred music platform.")
    else:
        speak("Sorry, I couldn't find that song in your playlist.")

def tell_joke():
    jokes = [
        "Why did the computer catch a cold? Because it left its Windows open!",
        "Why don’t programmers like nature? It has too many bugs!",
        "What is a programmer's favorite hangout place? Foo Bar!"
    ]
    speak(random.choice(jokes))


def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google.")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")
    elif "search google for" in c:
        query = c.replace("search google for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Here are the results for {query} on Google.")
    elif "search wikipedia for" in c:
        query = c.replace("search wikipedia for", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia, {result}")
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for this query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any information on Wikipedia.")
    elif "play" in c:
        song_name = c.replace("play", "").strip()
        play_song(song_name)
    elif "tell me a joke" in c:
        tell_joke()
    elif "what's the weather in" in c:
        city = c.replace("what's the weather in", "").strip()
        get_weather(city)
    elif "news update" in c:
        get_news()
    elif "shutdown" in c:
        speak("Shutting down your computer. Goodbye!")
        os.system("shutdown /s /t 5")
    else:
        speak("not found ")

if __name__ == "__main__":
    speak("Friday is ready.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=1)
            
            word = recognizer.recognize_google(audio)
            if word.lower() == "friday":
                speak("Yes, boss?")
                with sr.Microphone() as source:
                    print("Friday is activated")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)
        except sr.UnknownValueError:
            speak("once more")
        except sr.RequestError:
            speak("Network issue. Please check your internet connection.")
        except Exception as e:
            print("Error:", e)
            speak("Something went wrong.")
