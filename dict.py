import requests
import random
from colorama import Fore, init

init(autoreset=True)

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    data = r.json()
    return data[0]["meanings"][0]["definitions"][0]["definition"]

word_list = [
    "algorithm", "python", "keyboard", "computer",
    "science", "internet", "database", "network"
]

score = 0
total = 5

print(Fore.LIGHTMAGENTA_EX + "\n=== Dictionary Game ===")

for i in range(total):
    correct_word = random.choice(word_list)
    definition = get_definition(correct_word)

    if not definition:
        continue

    options = random.sample(word_list, 4)
    if correct_word not in options:
        options[0] = correct_word

    random.shuffle(options)

    print(Fore.MAGENTA + f"\nQ{i+1}. Definition:")
    print(definition)

    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")

    answer = input("Your answer (1-4): ")

    if answer.isdigit() and 1 <= int(answer) <= 4:
        if options[int(answer) - 1] == correct_word:
            print(Fore.GREEN + "Correct!")
            score += 1
        else:
            print(Fore.RED + f"Wrong! Correct answer: {correct_word}")
    else:
        print(Fore.RED + "Invalid choice!")

print(f"\nFinal Score: {score}/{total}")