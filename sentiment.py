from transformers import pipeline
from colorama import Fore, Style, init

init(autoreset=True)

classifier = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

total_count = 0
positive_count = 0
negative_count = 0

print(Fore.CYAN + Style.BRIGHT + "\nAI SENTIMENT ANALYSIS SYSTEM")
print(Fore.CYAN + "-" * 35)
print(Fore.YELLOW + "Enter any sentence to analyze sentiment")
print(Fore.YELLOW + "Type 'exit' to terminate the system")

while True:
    user_input = input(Fore.WHITE + "Input Text:").strip()

    if user_input.lower() == "exit":
        print(Fore.CYAN + "Session Summary")
        print(Fore.CYAN + "-" * 35)
        print(Fore.GREEN + f"Total inputs: {total_count}")
        print(Fore.GREEN + f"Positive    : {positive_count}")
        print(Fore.GREEN + f"Negative    : {negative_count}")
        print(Fore.CYAN + "\nSystem closed succesfully.\n")
        break

    if not user_input:
        print(Fore.RED + "\nInput cannot be empty.")
        continue

    result = classifier(user_input)[0]
    label = result["label"]
    confidence = round(result["score"] * 100, 2)

    total_count += 1

    if confidence >= 85:
        strength = "Strong"
    elif confidence >= 65:
        strength = "Moderate"
    else:
        strength = "Weak"

    if label == "POSITIVE":
        positive_count += 1
        color = Fore.GREEN
    else:
        negative_count += 1
        color = Fore.RED   

    print(color + Style.BRIGHT + "Analysis Result")
    print(color + "-" * 35)
    print(color + f"Sentiment     : {label}")
    print(color + f"Confidence    : {confidence}%")
    print(color + f"Strength level: {strength}")