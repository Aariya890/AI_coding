import requests
import json
from colorama import Fore, init

init(autoreset=True)

API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"
FILE_NAME = "facts.json"

def fetch_fact():
    try:
        r = requests.get(API_URL, timeout=5)
        return r.json().get("text") if r.status_code == 200 else None
    except:
        return None
    
def load_facts():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []
    
def save_fact(text):
    facts = load_facts()
    facts.append(text)
    with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2)

def show_facts():
    facts = load_facts()
    if not facts:
        print(Fore.LIGHTBLACK_EX + "No saved facts found.")
        return
    
    print(Fore.CYAN + "\n=== Saved facts ===")
    for i, fact in enumerate(facts, 1):
        print(Fore.GREEN + f"{i}. {fact}")

def menu():
    print(Fore.CYAN + "\n=== Random Fact Explorer ===")
    print(Fore.YELLOW + "[1] Get a new random fact")
    print(Fore.YELLOW + "[2] View saved facts")
    print(Fore.YELLOW + "[q] Quit")

def main():
    while True:
        menu()
        choice = input(Fore.WHITE + "Select: ").strip().lower()

        if choice == "q":
            break

        if choice == "1":
            fact = fetch_fact()
            if not fact:
                print(Fore.RED + "Falied to retrieve fact.")
                continue

            print(Fore.CYAN + "\n" + fact)
            if input(Fore.WHITE + "Save this fact? (y/n): ").lower() == "y":
                save_fact(fact)
                print(Fore.GREEN + "Saved succesfully.")

        elif choice == "2":
            show_facts()

        else:
            print(Fore.RED + "Invalid selection.")


if __name__ == "__main__":
    main()