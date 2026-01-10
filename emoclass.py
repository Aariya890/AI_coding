import sys
import joblib
import numpy as np
from colorama import Fore, Style, init
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

init(autoreset=True)

DATA_TRAINING = [
    ("I woke up this morning with a big smile on my face and excitement in my heart", "Happiness"),
    ("The good news filled me with joy and made my whole day brighter", "Happiness"),
    ("I could not stop laughing as we shared stories and jokes together", "Happiness"),
    ("Seeing my friends after a long time made me feel truly happy", "Happiness"),
    ("I felt a warm sense of contentment as I watched the sunset", "Happiness"),
    ("Her kind words lifted my mood and filled me with happiness", "Happiness"),
    ("I am happy knowing that all my hard work finally paid off", "Happiness"),
    ("The cheerful music instantly put me in a great mood", "Happiness"),
    ("I felt light and carefree, enjoying every moment of the day", "Happiness"),
    ("Happiness washed over me as I realized how grateful I was", "Happiness"),

    ("I felt a heavy ache in my chest as I sat alone in silence", "Sadness"),
    ("Tears quietly rolled down my face when I heard the news.", "Sadness"),
    ("The empty room made me feel lonelier than ever", "Sadness"),
    ("I struggled to smile, even though I knew I should", "Sadness"),
    ("My heart felt broken, and everything seemed darker", "Sadness"),
    ("I stared out the window, feeling lost and hopeless", "Sadness"),
    ("The disappointment weighed on me all day long.", "Sadness"),
    ("I missed them deeply, and the sadness would not fade", "Sadness"),
    ("It hurt to remember what I had lost.", "Sadness"),
    ("I went to bed feeling drained and full of sorrow.", "Sadness"),

    ("My fists clenched as frustration boiled inside me", "Anger"),
    ("I could feel my face grow hot with rage", "Anger"),
    ("Every word they said only made me angrier", "Anger"),
    ("I slammed the door, unable to hold back my anger", "Anger"),
    ("My patience snapped, and I raised my voice", "Anger"),
    ("The unfairness of the situation made my blood boil.", "Anger"),
    ("I struggled to stay calm, but irritation took over", "Anger"),
    ("Anger surged through me, sharp and uncontrollable", "Anger"),
    ("I shot them a glare, barely containing my fury", "Anger"),
    ("I paced back and forth, seething with anger", "Anger"),

    ("My heart raced as I heard footsteps behind me in the dark", "Fear"),
    ("A chill ran down my spine, and I froze in place", "Fear"),
    ("I held my breath, afraid to make a single sound", "Fear"),
    ("Panic tightened my chest, making it hard to breathe", "Fear"),
    ("My hands trembled as I reached for the door", "Fear"),
    ("I felt a sudden wave of terror wash over me", "Fear"),
    ("The shadows seemed to move, filling me with dread", "Fear"),
    ("Fear kept me rooted to the spot, unable to run", "Fear"),
    ("My stomach dropped when I realized I was not alone", "Fear"),
    ("I glanced around nervously, expecting something terrible to happen", "Fear"),

    ("I wrinkled my nose at the foul smell in the room", "Disgust"),
    ("The sight of the spoiled food made my stomach churn", "Disgust"),
    ("I felt sick just looking at the sticky, dirty floor", "Disgust"),
    ("A wave of revulsion hit me as I touched the slimy surface", "Disgust"),
    ("I turned away quickly, trying not to gag", "Disgust"),
    ("The taste was so unpleasant that I spat it out immediately", "Disgust"),
    ("My face twisted in disgust at the disturbing scene", "Disgust"),
    ("I shuddered at the thought of what had been left behind.", "Disgust"),
    ("Every instinct told me to step back and avoid it", "Disgust"),
    ("I felt nauseated and repelled by the mess in front of me", "Disgust"),
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
        return "Disgust", 0.0

    probs = model.predict_proba(X)[0]
    idx = np.argmax(probs)
    return model.classes_[idx], round(probs[idx] * 100, 2)

def main():
    print(Fore.CYAN + Style.BRIGHT + "\nEMOTION CLASSIFIER")
    print(Fore.CYAN + "-" * 55)
    print(Fore.YELLOW + "NLP system for emotion classification")
    print(Fore.YELLOW + "Type 'exit' to close\n")

    vectorizer, model = load_model()

    while True:
        text = input(Fore.WHITE + "Input Text: ").strip()

        if text.lower() == "exit":
            print(Fore.CYAN + "\nSystem terminated successfully.\n")
            sys.exit()

        if not text:
            print(Fore.RED + "Input cannot be empty.\n")
            continue

        label, confidence = analyze(text, vectorizer, model)

        print(Fore.GREEN + Style.BRIGHT + "\nClassification Result")
        print(Fore.GREEN + "-" * 55)
        print(f"Predicted Label : {label}")
        print(f"Confidence      : {confidence}%\n")

if __name__ == "__main__":
    main()