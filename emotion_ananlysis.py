from transformers import pipeline
from colorama import Fore, Style, init

init(autoreset=True)

emotion_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

EMOTION = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "fear",
    "surprise": "happy",
    "disgust": "angry",
    "neutral": "happy"
}

def detect_emotion(text):
    results = emotion_pipeline(text)[0]

    final_scores = {
        "happy": 0.0,
        "sad": 0.0,
        "angry": 0.0,
        "fear": 0.0
    }

    for r in results:
        mapped_emotion = EMOTION[r["label"]]
        final_scores[mapped_emotion] += r["score"]

    detected_emotion = max(final_scores, key=final_scores.get)
    return detected_emotion, final_scores


print(Fore.MAGENTA + Style.BRIGHT + "\nAI EMOTION DETECTION SYSTEM")
print(Fore.MAGENTA + "-" * 35)
print(Fore.YELLOW + "Enter any sentence to analyze your emotion")
print(Fore.YELLOW + "Type 'exit' to terminate the system")


while True:
    text = input(Fore.CYAN + "\nEnter text: ")

    if text.lower() == "exit":
        print(Fore.RED + "Exiting system...")
        break

    emotion, scores = detect_emotion(text)

    print(Fore.GREEN + "\nDetected Emotion: " + emotion.upper())
    print(Fore.GREEN + "Confidence Scores:")
    for k, v in scores.items():
        print(f"{k}: {v:.2f}")

    print(Fore.MAGENTA + "-" * 35)