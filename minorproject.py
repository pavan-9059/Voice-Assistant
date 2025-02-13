#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import speech_recognition as sr
import pyttsx3 as p
import random
import math 
import warnings
import os
from googlesearch import search
from pyjokes import get_joke
import randfacts
from pyowm import OWM
from selenium import webdriver
import datetime
import webbrowser
import requests
from word2number import w2n
import spotipy
from spotipy.oauth2 import SpotifyOAuth

engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')

current_language = "American English"
engine.setProperty('voice', voices[1].id)

warnings.filterwarnings("ignore")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 19:
        return "Evening"
    else:
        return "Night"

def quit_app():
    hour = int(datetime.datetime.now().hour)
    if 3 <= hour < 18:
        speak("Have a good day, sir")
    else:
        speak("Goodnight, sir")
    exit(0)
    
def get_news():
    api_key = ''
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        articles = news_data['articles']
        top_news = articles[:5]
        
        news_list = []
        for i, article in enumerate(top_news, start=1):
            news = f"News {i}: {article['title']}"
            news_list.append(news)
            print(news)
            speak(news)
            
    except Exception as e:
        print("Error while fetching news:", str(e))
        speak("Sorry, I couldn't fetch the news at the moment.")
        
def get_temperature(city):
    api_key = ''
    try:
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']
        description = weather.detailed_status

        speak(f"Temperature in {city} is {temp} degrees Celsius with {description}")
        print(f"Temperature in {city} is {temp} degrees Celsius with {description}")

    except Exception as e:
        print("Error fetching temperature:", str(e))
        speak("I couldn't fetch the temperature. Please check the city name.")
        
def get_number_input(prompt):
    retries = 5
    for attempt in range(retries):
        speak(prompt)
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, duration=1.2)
            print("Listening...")
            try:
                audio = r.listen(source)
                recognized_text = r.recognize_google(audio)
                print(f"Recognized text: {recognized_text}")
                
                try:
                    number = w2n.word_to_num(recognized_text)
                    return number
                except ValueError:
                    if recognized_text.isdigit():
                        return int(recognized_text)
                    speak("I couldn't interpret that as a number. Please try again.")
            except sr.UnknownValueError:
                speak("I didn't catch that. Please say the number again.")
            except Exception as e:
                print("Error:", e)
                speak("There was an error. Please try again.")
    speak("I'm sorry, I couldn't understand the number. Let's try something else.")
    return None

def change_language():
    global current_language
    speak("Which language do you want? American English or British English?")
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, duration=1.2)
        print("Listening for language preference...")
        audio = r.listen(source)
        language_choice = r.recognize_google(audio).lower()

    if "american" in language_choice:
        engine.setProperty('voice', voices[1].id)
        current_language = "American English"
        speak("Language changed to American English.")
    elif "british" in language_choice:
        engine.setProperty('voice', voices[2].id)
        current_language = "British English"
        speak("Language changed to British English.")
    else:
        speak("I couldn't understand your choice. Keeping the current language.")
    print(f"Current language: {current_language}")

def main_game_logic():
    speak("Let's start the number guessing game.")
    
    lower = get_number_input("Please say your lower limit.")
    if lower is None:
        return

    upper = get_number_input("Please say your upper limit.")
    if upper is None:
        return

    if lower >= upper:
        speak("The lower limit should be less than the upper limit. Let's restart the game.")
        return

    x = random.randint(lower, upper)
    chances = round(math.log(upper - lower + 1, 2))
    speak(f"You have {chances} chances to guess a number between {lower} and {upper}. Good luck!")

    count = 0
    while count < chances:
        count += 1
        guess = get_number_input(f"Attempt {count}: Guess a number.")
        if guess is None:
            continue

        if x == guess:
            speak(f"Congratulations! You guessed it in {count} attempts.")
            print(f"Congratulations, you did it in {count} tries!")
            break
        elif x > guess:
            speak("Your guess is too low.")
            print("You guessed too small!")
        else:
            speak("Your guess is too high.")
            print("You guessed too high!")

    if count >= chances:
        speak(f"Sorry, you've used all your chances. The correct number was {x}. Better luck next time!")
        print(f"\nThe number was {x}. Better luck next time!")
        
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""

scope = "user-read-playback-state,user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

PLAYLIST_URI = "spotify:playlist:?si=ATTxlIzTQ4mju5iQXs8fnA"
        
def play_spotify_playlist():
    try:
        spotify.start_playback(context_uri=PLAYLIST_URI)
        speak("Playing your Spotify playlist.")
    except Exception as e:
        print("Error playing Spotify playlist:", e)
        speak("An error occurred while trying to play your playlist. Please check your Spotify connection.")
        
def listen():
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, duration=1.2)
        print("Listening...")
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you repeat?")
            return None
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")
            return None
        
def get_directions():
    speak("Please tell me the location you want directions to.")
    location = listen()
    if location:
        speak(f"Fetching directions to {location}. Opening Google Maps.")
        webbrowser.open(f"https://www.google.com/maps/dir/?api=1&destination={location.replace(' ', '+')}")
    else:
        speak("I couldn't understand the location. Please try again.")

r = sr.Recognizer()

def main():
    speak("Hello sir, good " + wish_me() + ", I'm here to assist you.")
    speak("How are you?")
    
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, duration=1.2)
        print("Listening")
        audio = r.listen(source)
        text = r.recognize_google(audio)

    if "what about you" in text:
        speak("I am also having a good day")

    while True:
        speak("What can I do for you?")

        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, duration=1.2)
            print('Listening')
            audio = r.listen(source)
            text2 = r.recognize_google(audio)

        if "information" in text2:
            speak("You need information related to which topic?")
            
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, duration=1.2)
                print('Listening')
                audio = r.listen(source)
                info = r.recognize_google(audio)
            
            speak(f"Searching {info} on Wikipedia")
            print(f"Searching {info} on Wikipedia")
            
            driver = webdriver.Chrome()
            driver.get(f"https://en.wikipedia.org/wiki/{info.replace(' ', '_')}")

        elif "play video" in text2:
            speak("Which video do you want me to play?")
            
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, duration=1.2)
                print('Listening')
                audio = r.listen(source)
                vid = r.recognize_google(audio)
            
            speak(f"Playing {vid} on YouTube")
            print(f"Playing {vid} on YouTube")
            url = f"https://www.youtube.com/results?search_query={vid.replace(' ', '+')}"
            webbrowser.open(url) 

        elif "present" in text2:
            speak("Fetching the latest news for you, sir.")
            get_news()

        elif "temperature" in text2:
            speak("Please specify the city for which you want the temperature")
            
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, duration=1.2)
                print('Listening')
                audio = r.listen(source)
                city = r.recognize_google(audio)
            
            get_temperature(city)

        elif "funny" in text2:
            speak("Get ready for some chuckles")
            joke = get_joke()
            speak(joke)
            print(joke)

        elif "your name" in text2:
            speak("My name is Next Gen Optimal Voice Assistant Nova")

        elif "fact" in text2:
            speak("Sure sir, did you know that...")
            fact = randfacts.getFact()
            speak(fact)
            print(fact)

        elif "search" in text2:
            speak("What should I search for, sir?")
            
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, duration=1.2)
                print('Listening')
                audio = r.listen(source)
                query = r.recognize_google(audio)
            
            speak(f"Searching {query} on Google")
            print(f"Searching {query} on Google")
            results = search(query, num_results=5)
            
            speak("Here are the top results:")
            for idx, result in enumerate(results, start=1):
                print(f"Result {idx}: {result}")
                #speak(f"Result {idx}: {result}")

        elif "game" in text2:
            main_game_logic()
            
        elif "reboot the system" in text2:
            speak("Do you wish to restart your computer?")
            
            with sr.Microphone() as source:
                r.energy_threshold = 10000
                r.adjust_for_ambient_noise(source, duration=1.2)
                print('Listening')
                audio = r.listen(source)
                restart = r.recognize_google(audio)
            
            if "yes" in restart.lower():
                os.system("shutdown /r /t 1")

        elif "light off" in text2:
            speak("I no longer control the lights.")
            # We need smart led lights like Philips Hue and we have to use python library called phue.
            
        elif "change the language" in text2:
                change_language()
                
        elif "play songs" in text2:
                    play_spotify_playlist()
                
        elif "directions" in text2:
                get_directions()

        elif "stop" in text2 or "exit" in text2 or "end" in text2:
            speak("It's a pleasure helping you, and I am always here to assist.")
            quit_app()

main()


# In[ ]:





# In[ ]:




