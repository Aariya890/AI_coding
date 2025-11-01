from colorama import Fore, Style, init
import random
import time

init(autoreset=True)

study_tips = [
    "Plan your study sessions with clear goals.",
    "Review lessons daily to strengthen memory.",
    "Teach others - it's one of the best ways to learn.",
    "Avoid multitasking during study time.",
    "Sleep well - memory retention increases with rest.",
    "Never give up - mistakes are the proof that you are trying.",
    "Stay organized notes and materials."
    
]

motivational_quotes = [
    "There are two ways to live; one is everything is a mistery and nothing is a mistery.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "The most effective way to do it, is to do it.",
    "It always seems impossible until it's done.",
    "Push yourself, because no one else is going to do it for you.",
    "It does not matter how slowly you go as long as you do not stop."
]

subject_help = [
    "Math": "Math is like exercise — the more you practice, the stronger your skills get.",
    "English": "Read books, newspapers, or online articles to learn new words and sentence structures.",
    "Science": "Don’t just memorize — try to understand why and how things happen.",
    "History": "Focus on the events, causes, and effects — think of history as a story, not just facts to memorize.",
    "Geography": "Practice locating countries, rivers, mountains, and cities — the more you look at maps, the better your memory gets.",
    "Computer": "The more you use a computer, the more comfortable and confident you will become.",
]

def  display_menu():
    print(Fore.CYAN + "=====Student Helper Menu =====")
    print(Fore.YELLOW + "1. Get Study Tips")
    print("2. Get Motivational Quote")
    print("3. Subject help")
    print("4. Create Study Routine")
    print("5. Chat freely")
    print("6. Exit")
    print(Fore.CYAN + "==============================\n")
    
def generate_study_routine():
    routine = {
        "Morning": "Study new or difficult topics when your mind is fresh"
        "Afternoon": "Practice problems and apply what you’ve learned."
        "Night": "Review the day’s work and plan for tomorrow."
    }    
    print(Fore.GREEN + "\nRecommended sudy routine: ")
    for k, v in routine.items():
        print(Fore.GREEN + f"{k} : {v}")
    print()

def chat_freely():
        
    