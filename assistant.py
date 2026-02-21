import speech_recognition as sr
import pyttsx3
import datetime
import time
import webbrowser
import os

engine = pyttsx3.init()
engine.setProperty("rate", 145)

listener = sr.Recognizer()

tasks = []

def speak(text):
    print("Assistant: ", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)

def listen():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=0.4)
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        print("User: ", command)
        return command.lower()
    except:
        return ""
    
def add_task(task):
    tasks.append(tasks)
    return "Task added succesfully."

def list_tasks():
    if not tasks:
          return "You have no tasks."
    return "Your tasks are:" + ", ".join(tasks)

def clear_tasks():
    tasks.clear()
    return "All tasks are cleared."

def generate_reply(command):

    if "exit" in command or "stop" in command:
        speak("Session terminated. Have a nice day.")
        exit()

    if "time" in command:
        return datetime.datetime.now().strftime("Current time is %I:%M %p.")
    
    if "date" in command:
        return datetime.datetime.now().strftime("Today's date is %B %d, %Y.")
    
    if "add task" in command:
        task = command.replace("search", "").strip()
        if task:
            return add_task(task)
        return "Please say the task name."
    
    if "list tasks" in command:
        return list_tasks()

    if "clear tasks" in command:
        return clear_tasks()

    if "search" in command:
        query = command.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query}"
        return "Please say what you want to search."
    
    if "open youtube" in command:
            webbrowser.open(f"https://youtube.com")
            return "Opening Youtube."
    
    if "open google" in command:
            webbrowser.open(f"https://google.com")
            return "Opening Google."
    

    return "Command not recognised. Please try again."

def main():
     speak("Smart assistant is ready. Awaiting your command.")

     while True:
        command = listen()
        if command:
            reply = generate_reply(command)
            speak(reply)

if __name__ == "__main__":
    main()