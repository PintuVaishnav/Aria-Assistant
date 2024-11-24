import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import urllib.parse

# Initialize speech recognition and text-to-speech engine
recog = sr.Recognizer()
ttsx = pyttsx3.init()

def speak(text):
    """Speak the given text."""
    ttsx.say(text)
    ttsx.runAndWait()

def processcommand(command):
    """Process the given command and take appropriate actions."""
    command = command.strip().lower()

    if "open" in command:
        is_incognito = "incognito" in command
        site_name = command.replace("open", "").replace("incognito", "").strip().lower()

        if "play" in command:
            task_site = site_name.split("play")[0].strip()
            task_content = command.split("play")[1].strip()

            speak(f"Opening {task_site} and playing {task_content}")

            if "spotify" in task_site:
                webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(task_content)}")

            elif "youtube" in task_site:
                search_query = urllib.parse.quote(task_content)
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                webbrowser.open(f"https://www.youtube.com/watch?v={search_query}")
            
            else:
                speak(f"Sorry, I don't know how to play content on {task_site}.")

        elif "search" in command:
            task_site = site_name.split("search")[0].strip()
            search_query = command.split("search for")[1].strip() if "search for" in command else ""
            speak(f"Searching for {search_query} on {task_site}")

            if "google" in task_site:
                if is_incognito:
                    subprocess.run(["chrome", "--incognito", f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"])
                else:
                    webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(search_query)}")

            elif "youtube" in task_site:
                if is_incognito:
                    subprocess.run(["chrome", "--incognito", f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"])
                else:
                    webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}")
            
            elif "linkedin" in task_site:
                webbrowser.open(f"https://www.linkedin.com/search/results/people/?keywords={urllib.parse.quote(search_query)}")
            
            elif "twitter" in task_site:
                webbrowser.open(f"https://twitter.com/search?q={urllib.parse.quote(search_query)}")
            
            elif "wikipedia" in task_site:
                webbrowser.open(f"https://en.wikipedia.org/wiki/{urllib.parse.quote(search_query)}")
            
            else:
                speak(f"Sorry, I don't know how to search on {task_site}.")

        else:
            speak(f"Opening {site_name}")
            if is_incognito:
                subprocess.run(["chrome", "--incognito", f"https://www.{site_name}.com"])
            else:
                webbrowser.open(f"https://www.{site_name}.com")

    else:
        speak("Sorry, I didn't understand the command.")

def listen_for_command():
    """Listen for commands from the user."""
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source)
        print("Listening for 'hello' to activate...")

        try:
            audio = recog.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout and phrase time limit
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
            if "hello" in command:
                speak("Yes, how can I assist you?")
                print("Listening for your command...")

                # Allow the assistant to listen for the next command
                command = listen_for_command()  # Wait for next command after activation phrase
                if command:
                    processcommand(command)

            else:
                print("Listening for 'hello' to activate...")
                speak("Say 'hello' to activate the assistant.")
