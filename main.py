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
    "Stay organized with your notes and materials."
]

motivational_quotes = [
    "There are two ways to live: one is everything is a mystery and the other is nothing is a mystery.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "The most effective way to do it, is to do it.",
    "It always seems impossible until it's done.",
    "Push yourself, because no one else is going to do it for you.",
    "It does not matter how slowly you go as long as you do not stop."
]

subject_help = {
    "math": "Math is like exercise — the more you practice, the stronger your skills get.",
    "english": "Read books, newspapers, or online articles to learn new words and sentence structures.",
    "science": "Don’t just memorize — try to understand why and how things happen.",
    "history": "Focus on the events, causes, and effects — think of history as a story, not just facts to memorize.",
    "geography": "Practice locating countries, rivers, mountains, and cities — the more you look at maps, the better your memory gets.",
    "computer": "The more you use a computer, the more comfortable and confident you will become.",
}

def display_menu():
    print(Fore.CYAN + "===== Student Helper Menu =====")
    print(Fore.YELLOW + "1. Get Study Tips")
    print("2. Get Motivational Quote")
    print("3. Subject Help")
    print("4. Create Study Routine")
    print("5. Chat Freely")
    print("6. Exit")
    print(Fore.CYAN + "===============================\n")

def generate_study_routine():
    routine = {
        "Morning": "Study new or difficult topics when your mind is fresh.",
        "Afternoon": "Practice problems and apply what you’ve learned.",
        "Night": "Review the day’s work and plan for tomorrow."
    }
    print(Fore.GREEN + "\nRecommended study routine:")
    for k, v in routine.items():
        print(Fore.GREEN + f"{k}: {v}")
    print()

def chat_freely():
    print(Fore.CYAN + "\nBot: You can chat with me! Type 'back' to return to the menu.\n")
    while True:
        query = input(Fore.YELLOW + "You: ").lower().strip()
        if query == 'back':
            break
        elif "study" in query:
            print(Fore.GREEN + "Bot: Sleep well - memory retention increases with rest.")
        elif "motivation" in query:
            print(Fore.MAGENTA + "Bot: " + random.choice(motivational_quotes))
        elif any(sub in query for sub in subject_help):
            for sub in subject_help:
                if sub in query:
                    print(Fore.BLUE + f"Bot: {subject_help[sub]}")
                    break
        elif "thank" in query:
            print(Fore.CYAN + "Bot: You are welcome! Keep working hard.")
        else:
            print(Fore.RED + "Bot: I'm still learning to respond better. Try to ask about study, motivation, or subjects.")

def student_helper_bot():
    print(Fore.CYAN + "Student Helper Bot: Hello! I'm your AI study companion.")
    time.sleep(0.5)
    print(Fore.CYAN + "Let's get started!\n")
    
    while True:
        display_menu()
        choice = input(Fore.YELLOW + "Enter your choice (1-6): ").strip()
        
        if choice == "1":
            print(Fore.GREEN + "\nBot: Here's a useful study tip for you —")
            print(Fore.GREEN + random.choice(study_tips))
            
        elif choice == "2":
            print(Fore.MAGENTA + "\nBot: " + random.choice(motivational_quotes))    
            
        elif choice == "3":
            subject = input(Fore.YELLOW + "\nEnter the subject (Math, Science, English, History, Geography, Computer): ").lower().strip()
            if subject in subject_help:
                print(Fore.BLUE + "Bot: " + subject_help[subject])        
            else:
                print(Fore.RED + "Bot: Sorry, I don't have specific advice for that subject yet.")   
              
        elif choice == "4":  
            generate_study_routine()   
            
        elif choice == "5": 
            chat_freely()  
             
        elif choice == "6": 
            print(Fore.CYAN + "Bot: Goodbye! Keep studying and stay positive.")
            break
        else: 
            print(Fore.RED + "Bot: Invalid option. Please select from 1-6.")   

if __name__ == "__main__":
    student_helper_bot()
