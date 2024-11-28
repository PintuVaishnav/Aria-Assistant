import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import requests
import re

recog = sr.Recognizer()
ttsx = pyttsx3.init()

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

def fetch_definition_online(query):
    try:
        response = requests.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "Sorry, I couldn't find information on that.")
        else:
            return "Sorry, I couldn't find information on that."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def answer_question(question):
    query = question.replace("what is", "").replace("who is", "").replace("define", "").strip()
    speak("Let me find that for you.")
    answer = fetch_definition_online(query)
    speak(answer)
    print(answer)

def processcommand(command):
    command = command.strip().lower()

    if command.startswith("what is") or command.startswith("who is") or command.startswith("define"):
        answer_question(command)
    elif "open" in command:
        site_name = command.replace("open", "").strip()
        if "spotify" in command and "my songs" in command:
            speak("Opening Spotify and playing your songs.")
            webbrowser.open("https://open.spotify.com/collection/tracks")
        elif "Spotify" in command and "play next song" in command:
            speak("Playing the next song on Spotify.")
            webbrowser.open("https://open.spotify.com/collection/tracks")
        elif "gemini" in command or "gemini ai" in command:
            speak("Opening Gemini AI.")
            webbrowser.open("https://gemini.google.com/")
        elif "brave" in command:
            speak("Opening Brave Browser." if not command.endswith(("on brave", "on brave browser", "brave browser", "in brave browser", "in brave")) else f"Opening {command.replace('on brave', '').replace('browser', '').strip()} on Brave Browser.")
            webbrowser.open(f"https://search.brave.com/search?q={urllib.parse.quote(command.replace('on brave', '').replace('browser', '').strip())}" if command.endswith(("on brave", "on brave browser", "brave browser", "in brave browser", "in brave")) else "https://search.brave.com/")

        elif "spotify" in command:
            task_content = command.replace("open spotify and play", "").strip()
            if task_content:
                speak(f"Playing {task_content} on Spotify.")
                webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(task_content)}")
            else:
                speak("Opening Spotify.")
                webbrowser.open("https://open.spotify.com/")
        elif "youtube" in command and "play" in command:
            task_content = command.split("play")[1].strip()
            search_query = urllib.parse.quote(task_content)
            speak(f"Playing {task_content} on YouTube.")

            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            response = requests.get(search_url)
    
            video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
            if video_ids:
                first_video_url = f"https://www.youtube.com/watch?v={video_ids[0]}"
                webbrowser.open(first_video_url)
        elif "chatgpt" in command or "chat gpt" in command or "gpt" in command:
            speak("Opening ChatGPT.")
            webbrowser.open("https://chatgpt.com/")    
        else:
            speak(f"Opening {site_name}")
            webbrowser.open(f"https://www.{site_name}.com")
    else:
        speak("Sorry, I didn't understand the command.")

def listen_for_command():
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source)
        print("Listening for 'Hello Aria' to activate...")
        try:
            print("Listening for command...")
            audio = recog.listen(source, timeout=10, phrase_time_limit=10)
            command = recog.recognize_google(audio)
            print(f"Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected within the expected time.")
            return None

if __name__ == "__main__":
    speak("Activating Aria-Assistant")
    while True:
        command = listen_for_command()
        if command:
            if "hello" in command or "aria" in command or "arya" in command or "hey" in command:
                speak("Yes, how can I assist you?")
                command = listen_for_command()
                if command:
                    processcommand(command)
            elif "goodbye" in command or "exit" in command:
                speak("Goodbye!")
                exit()
            else:
                print("Listening for 'Hello Aria' to activate...")
