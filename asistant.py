import speech_recognition as sr
import pyttsx3
import datetime
import time
import sys

listener = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 145)

user_name = None
expecting_name = False

def speak(text):
    print("Assistant: ", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.4)

def listen():
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=0.5)
        audio = listener.listen(source)
        
    try:
        text = listener.recognize_google(audio)
        print("User: ", text)
        return text.lower()
    except:
        return ""
    
def generate_reply(text):
    global user_name, expecting_name

    if text in ["exit", "stop", "quit", "goodbye", "bye"]:
        print("Goodbye! Have a wonderful day.")
        sys.exit(0)

    if expecting_name:
        user_name = text.title()
        expecting_name = False
        return f"Nice to meet you {user_name}. I will remember your name."
    
    if "hello" in text or "hi" in text or "hey" in text:
        if user_name:
            return f"Hello {user_name}. How are you today?"
        expecting_name = True
        return "Hello. What is your name?"
    
    if "my name is" in text:
        user_name = text.replace("my name is", "").strip().title()
        return f"Nice to meet you {user_name}. I will remember your name."
    
    if "what is my name" in text:
        if user_name:
            return f"Your name is {user_name}."
        expecting_name = True
        return "I do not know your name yet. Please tell me your name."
    
    if "time" in text:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    
    if "date" in text or "today" in text:
        return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}"
    
    if "how are you" in text:
        return "I am doing great. Thank you for asking."
    
    if "what can you do" in text:
        return "I can talk with you, tell time and date, and remember your name."
    
    return "You said " + text

def main():
    print("Voice assistant started. You may speak now.")

    while True:
        text = listen()
        if text:
            reply = generate_reply(text)
            if reply:
                speak(reply)


if __name__ == "__main__":
    main()                