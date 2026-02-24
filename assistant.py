import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
from colorama import Fore, init
import time

init(autoreset=True)

# Initialize speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

recognizer = sr.Recognizer()

languages = {
    "spanish": "es",
    "arabic": "ar",
    "korean": "ko",
    "japanese": "ja",
    "german": "de"
}

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio, language="en-US").lower()
    except:
        return ""

def select_language():
    speak("Please say your target language. Spanish, Arabic, Korean, Japanese, or German.")
    print(Fore.CYAN + "\nListening for language selection...")

    spoken_lang = listen()

    print(Fore.YELLOW + f"Detected: {spoken_lang}")

    return languages.get(spoken_lang)

def main():

    print(Fore.GREEN + "\nVoice Translation Assistant Activated\n")
    speak("Voice translation system activated.")

    while True:

        target_language = select_language()

        if not target_language:
            speak("Invalid language detected. Please try again.")
            continue

        translator = GoogleTranslator(source="en", target=target_language)

        speak("Language selected. You may now speak your sentence.")

        while True:

            print(Fore.CYAN + "\nListening...")
            sentence = listen()

            if not sentence:
                speak("I did not catch that. Please repeat.")
                continue

            print(Fore.YELLOW + f"You said: {sentence}")

            if "exit" in sentence:
                speak("System shutdown completed.")
                return

            if "change language" in sentence:
                speak("Switching language.")
                break

            try:
                translated = translator.translate(sentence)
                print(Fore.MAGENTA + f"Translated Output: {translated}")
                speak(translated)

            except Exception as e:
                print(Fore.RED + f"Translation error: {e}")
                speak("Processing error occurred.")

if __name__ == "__main__":
    main()