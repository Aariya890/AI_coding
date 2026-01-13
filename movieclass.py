import sys
import joblib
import numpy as np
from colorama import Fore, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

init(autoreset=True)

MOVIES = [
    "Comedy",
    "Thriller",
    "Romance",
    "Horror",
    "Sci-Fi"
]

DATA_TRAINING = [
   ("Superbad", "Comedy"),
   ("Accepted", "Comedy"),
   ("Dumb and Dumber", "Comedy"),
   ("White Chicks", "Comedy"),
   ("Vacation", "Comedy"),

   ("The call", "Thriller"),
   ("Game Over", "Thriller"),
   ("Psycho", "Thriller"),
   ("Deep Water", "Thriller"),
   ("Taxi Driver", "Thriller"),

   ("Call me by your name", "Romance"),
   ("My Oxford year", "Romance"),
   ("Remember me", "Romance"),
   ("The idea of you", "Romance"),
   ("The holiday", "Romance"),

   ("The Shining", "Horror"),
   ("Halloween", "Horror"),
   ("The Ring", "Horror"),
   ("A Nightmare of Elm street", "Horror"),
   ("It", "Horror"),

   ("Gravity", "Sci-Fi"),
   ("Jurrasic Park", "Sci-Fi"),
   ("Back to the Future", "Sci-Fi"),
   ("Super 8", "Sci-Fi"),
   ("Frankenstein", "Sci-Fi"),
]

def train_model():
    texts = [x[0] for x in DATA_TRAINING]
    labels = [x[1] for x in DATA_TRAINING]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)

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
        print(Fore.YELLOW + "Training local NLP model...")
        train_model()
        return load_model()

def analyze(text, vectorizer, model):
    X = vectorizer.transform([text])
    if X.nnz == 0:
        return "Sci-Fi", 0.0

    probs = model.predict_proba(X)[0]
    idx = np.argmax(probs)
    return model.classes_[idx], round(probs[idx] * 100, 2)

def main():
    print(Fore.CYAN + Style.BRIGHT + "\nMOVIE TYPE CLASSIFIER")
    print(Fore.CYAN + "-" * 55)
    print(Fore.YELLOW + "NLP system for Movie type classification")
    print(Fore.YELLOW + "Type 'exit' to close\n")

    vectorizer, model = load_model()

    while True:
        text = input(Fore.WHITE + "Input a name of a movie: ").strip()

        if text.lower() == "exit":
            print(Fore.CYAN + "\nSystem terminated successfully.\n")
            sys.exit()

        if not text:
            print(Fore.RED + "Input cannot be empty.\n")
            continue

        label, confidence = analyze(text, vectorizer, model)

        print(Fore.GREEN + Style.BRIGHT + "\nClassification Result")
        print(Fore.GREEN + "-" * 55)
        print(f"Predicted Movie type : {label}")
        print(f"Confidence      : {confidence}%\n")

if __name__ == "__main__":
    main()