import sys
import joblib
import numpy as np
from colorama import Fore, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

init(autoreset=True)

TRAIN_DATA = [
    ("My mind is filled with joy", "Happiness"),
    ("I am very happy", "Happiness"),
    ("I cannot stop smilling", "Happiness"),
    ("I am very grateful and pleased", "Happiness"),
    ("I am very delighted", "Happiness"),
    ("I was buzzing with happiness", "Happiness"),
    ("My heart was singing from joy", "Happiness"),
    
    ("I was crying hard", "Sadness"),
    ("Tears rolled down my face", "Sadness"),
    ("I feel empty", "Sadness"),
    ("My heart is heavy", "Sadness"),
    ("I am feeling deppressed", "Sadness"),

    ("My face turned red when I was angry", "Anger"),
    ("Blood was boiling of anger", "Anger"),
    ("I am very angry", "Anger"),
    ("He was glaring at me with anger", "Anger"),
    ("I clenched my teeth so tight that my teeth began to ache", "Anger")
]

def train_model():
    text = [x[0] for x in TRAIN_DATA]
    labels = [x[1] for x in TRAIN_DATA]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(text)

    model = MultinomialNB(alpha=1.5)
    model.fit(X, labels)

    joblib.dump(vectorizer, "vectorizer.pkl")
    joblib.dump(model, "intent_model.pkl")

def load_model():
    try:
        vectorizer = joblib.load("vectorizer.pkl")
        model = joblib.load("intent_model.pkl")
        return vectorizer, model
    
    except FileNotFoundError:
        print(Fore.YELLOW + "Training local model...")
        train_model()
        return load_model()

def analyze(text, vectorizer, model):
    X = vectorizer.transform([text])
    if X.nnz == 0:
        return "Anger", 0.0
    
    probs = model.predict_proba(X)[0]
    idx = np.argmax(probs)
    return model.classes_[idx], round(probs[idx] * 100, 2)

def main():
    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "EMOTION CLASSIFIER")
    print(Fore.LIGHTBLACK_EX  + "-" * 35)
    print(Fore.MAGENTA + "NLP system for emotion classification...")
    print(Fore.MAGENTA + "Type 'exit' to quit\n")

    vectorizer, model = load_model()

    while True:
        text = input(Fore.CYAN + "Input text: ").strip()
        if text.lower() == "exit":
            print("System terminated succesfully.\n")
            sys.exit()

        if not text:
            print(Fore.RED + "Input cannot be empty.")
            continue

        label, confidence = analyze(text, vectorizer, model)
        
        print(Fore.GREEN + "Classification result:\n")
        print(Fore.GREEN + "-" * 35)
        print(f"Label : {label}")
        print(f"Confidence : {confidence}")

if __name__ == "__main__":
    main()