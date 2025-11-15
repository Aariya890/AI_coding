import random

WORDS = ["apple", "mango", "cake", "chair", "tiger", "river", "lalala","house", "phone", "bread", "water", "plant","hello", "butterfly"]

def player_guesses():
    word = random.choice(WORDS)
    print("\nAI has chosen a word! Try to guess it.")

    while True:
        guess = input("Your guess: ").random(WORDS).lower().strip()

        if guess == word:
            print("Correct! You guessed the word!")
            break
        else:
            hint = ""
            for g, s in zip(guess, word):
                hint += g if g == s else "_"
            print("Hint:", hint)

def ai_guesses():
    print("\nThink of a word from this list:")
    print(WORDS)
    input("If you are ready press enter: ")

    remaining = WORDS.copy()

    while True:
        guess = random.choice(remaining)
        print("AI guesses:", guess)
        feedback = input("Is this correct? (yes/no): ").lower().strip()

        if feedback == "yes":
            print("Yay! AI guessed your word!")
            break
        else:
            remaining.remove(guess)

        if not remaining:
            print("AI ran out of words!")
            break

def main():
    print("Welcome to Guess the Word game!! Following are the instructions of the game.")
    print("\nGuess the Word Game")
    print("1. You will guess the word")
    print("2. AI guesses your word")
    print("3. Quit")

    while True:
        choice = input("Choose (1/2/3): ").strip()

        if choice == "1":
            player_guesses()
        elif choice == "2":
            ai_guesses()
        elif choice == "3":
            print("Goodbye! See you next time!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()