from colorama import Fore, Style, init
import random
import time

init(autoreset=True)

Healthy_eating_tips = [
    "Aim for at least 5 servings a day for vitamins, minerals, and fiber.",
    "Go for brown rice, oats, or whole wheat bread instead of refined grains.",
    "Try fish, eggs, beans, lentils, or skinless chicken.",
    "Stay hydrated and limit sugary drinks.",
    "Too much can raise blood pressure and cause weight gain.",
    "Regular meals keep your metabolism and energy stable.",
    "Focus on your food and avoid eating while watching TV or using your phone."
]

Reasons = [
    "Healthy food provides the fuel your body needs to work, study, and play.",
    "Proteins, vitamins, and minerals help your body grow and repair itself.",
    "Nutrient-rich foods help you think clearly and concentrate better.",
    "Calcium and vitamin D from milk, fish, and greens support bone health.",
    "Fiber-rich foods keep your stomach healthy and prevent constipation.",
    "A healthy diet helps you live longer and stay active as you age."
]   
Food_habits = {
    "Fruits": "Full of vitamins and fiber — eat 2–4 servings a day (like one apple or a banana).",
    "Vegetables": "Keep your body healthy and strong — eat 3–5 servings a day (like one bowl of cooked veggies or salad).",
    "Fat": "Important for energy, but eat in small amounts — about 2 servings a day (like a teaspoon of oil or a few nuts).",
    "Water": "Very important for all body functions — drink 6–8 glasses a day.",
    "Protein": "Proteins: Build muscles and repair body tissues — eat 2–3 servings a day (like fish, egg, meat, beans, or lentils)."
}

def display_menu():
    print(Fore.CYAN + "===== Diet Helper Menu =====")
    print(Fore.YELLOW + "1. Get Healthy Eating Tips")
    print("2. Know Healthy food habit reasons")
    print("3. Know Healthy food habits")
    print("4. Create Healthy diet Routine")
    print("5. Chat Freely")
    print("6. Exit")
    print(Fore.CYAN + "===============================\n")

def generate_food_routine():
    routine = {
        "Morning": "Eat energy-giving foods to start your day.",
        "Afternoon": "Eat a balanced meal with all food groups.",
        "Night": "Eat light and easy-to-digest foods."
    }
    print(Fore.GREEN + "\nRecommended Healthy diet routine:")
    for k, v in routine.items():
        print(Fore.GREEN + f"{k}: {v}")
    print()

def chat_freely():
    print(Fore.CYAN + "\nBot: You can chat with me! Type 'back' to return to the menu.\n")
    while True:
        query = input(Fore.YELLOW + "You: ").lower().strip()
        if query == 'back':
            break
        elif "tips" in query or "eating" in query:
            print(Fore.GREEN + "Bot: ")
        elif "reasons" in query:
            print(Fore.MAGENTA + "Bot: " + random.choice(Reasons))
        elif any(sub in query for sub in Food_habits):
            for food in Food_habits:
                if food in query:
                    print(Fore.BLUE + f"Bot: {Food_habits[food]}")
                    break
        elif "thank" in query:
            print(Fore.CYAN + "Bot: You are welcome! Keep working hard.")
        else:
            print(Fore.RED + "Bot: I'm still learning to respond better. Try to ask about study, motivation, or subjects.")

def Diet_helper_bot():
    print(Fore.CYAN + "Diet Helper Bot: Hello! I'm your AI diet companion.")
    time.sleep(0.5)
    print(Fore.CYAN + "Let's get started!\n")
    
    while True:
        display_menu()
        choice = input(Fore.YELLOW + "Enter your choice (1-6): ").strip()
        
        if choice == "1":
            print(Fore.GREEN + "\nBot: Here's a useful healthy eating tip for you —")
            print(Fore.GREEN + random.choice(Healthy_eating_tips))
            
        elif choice == "2":
            print(Fore.MAGENTA + "\nBot: " + random.choice(Reasons))    
            
        elif choice == "3":
            food = input(Fore.YELLOW + "\nEnter the food type(protein, fruit, vegetable, fat, water): ").lower().strip()
            if food in Food_habits:
                print(Fore.BLUE + "Bot: " + Food_habits[food])        
            else:
                print(Fore.RED + "Bot: Sorry, I don't have specific advice for that type of foodyet.")   
              
        elif choice == "4":  
            generate_food_routine()   
            
        elif choice == "5": 
            chat_freely()  
             
        elif choice == "6": 
            print(Fore.CYAN + "Bot: Goodbye! Keep trying and stay healthy.")
            break
        else: 
            print(Fore.RED + "Bot: Invalid option. Please select from 1-6.")   

if __name__ == "__main__":
    Diet_helper_bot()
