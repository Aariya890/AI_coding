import requests
import random
import html
from colorama import init, Fore

init(autoreset=True)

def get_Data():
    url = "https://www.opentdb.com/api.php?amount=1&type=multiple"
    res = requests.get(url)
    data = res.json()

    if data["response_code"] != 0:
        return None
    q = data["results"][0]
    question = html.unescape(q["question"])
    correct = html.unescape(q["correct_answer"])
    incorrect = [html.unescape(i) for i in q["incorrect_answers"]]
    options = incorrect + [correct]
    random.shuffle(options)
    labels = ["A", "B", "C", "D"]
    mapped = dict(zip(labels, options))
    return question, correct, mapped


def askQuestion():
    data = get_Data()

    if not data:
        print(Fore.RED + "Unable to fetch question.")
        return False
    
    question, correct, mapped = data
    print(Fore.CYAN + "\n" + question)
    for label, text in mapped.items():
        print(Fore.YELLOW + f"{label}. {text}")
    choice = input(Fore.GREEN + "Choose your answer(A-D): ").upper().strip()

    if choice in mapped:
        if mapped[choice] == correct:
            print(Fore.BLUE + "Correct!")
            return True
        print(Fore.RED + f"Incorrect. Correct answer: {correct}\n")
        return False
    print(Fore.RED + "Invalid choice.\n")
    return False


def startQuiz():
   score = 0
   total = 10
   print(Fore.MAGENTA + "\n (:--- QUIZ GAME ---:) \n") 

   for _ in range(total):
        if askQuestion():
           score += 1

   print(Fore.MAGENTA + f"Final Score: {score}/{total}")
   
startQuiz()
   