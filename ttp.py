import pyttsx3
from deep_translator import GoogleTranslator
from colorama import Fore, init

init(autoreset=True)

engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def display_language_options():
    print(Fore.CYAN + "\nAvailable Translation Languages:")
    print("1. Spanish (es)")
    print("2. Japanese (ja)")
    print("3. Turkish (tr)")
    print("4. French (fr)")
    print("5. Korean (ko)")
    print("6. Bengali (bn)")
    print("7. Thai (th)")
    print("8. Arabic (ar)")
    print("0. Exit Program")

    return {
        "1" : "es",
        "2" : "ja",
        "3" : "tr",
        "4" : "fr",
        "5" : "ko",
        "6" : "bn",
        "7" : "th",
        "8" : "ar"
    }


def select_language():
    languages = display_language_options()
    choice =  input(Fore.YELLOW + "\nSelect Target Language(1-8): ").strip()

    if choice == "0":
        return None
    
    return languages.get(choice)


def main():
    print(Fore.GREEN + "\nText-Based TTS System Initialized. \n")

    while True:
        target_language = select_language()

        if target_language is None:
            print(Fore.GREEN + "System shutdown completed.")
            break

        translator = GoogleTranslator(source='en', target=target_language)

        print(Fore.CYAN + "\nTranslation engine ready. Enter  English text below.")
        print(Fore.YELLOW + "Type 'lang' to chage language or 'exit' to quit.\n")

        while True:
            text = input(Fore.YELLOW + ">>").strip()

            if text.lower() == "exit":
                print(Fore.GREEN + "\nSystem shutdown completed.")
                return

            if text.lower() == "lang":
                print(Fore.CYAN + "\nSwitching language selections...")
                break

            if not text:
                print(Fore.RED + "Empty input detected. Please input valid text.")
                continue

            try:
                translated = translator.translate(text)
                print(Fore.MAGENTA + f"Translated output: {translated}")
                speak(translated)

            except Exception as e:
                print(Fore.RED + f"Processing error : {e}")


if __name__ == "__main__":
    main()