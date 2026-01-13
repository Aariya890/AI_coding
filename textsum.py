from transformers import pipeline
from colorama import Fore, Style, init
import torch

init(autoreset=True)

class BarTextSummarizer:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.model_name = "facebook/bart-large-cnn"

        self.summarizer = pipeline(
            "summarization",
            model=self.model_name,
            device=self.device
        )

    def summarize(self, text):
        input_length = len(text.split())

        max_length = max(30, int(input_length * 0.6))
        min_length = max(15, int(max_length * 0.5))

        summary = self.summarizer(
            text,
            min_length=min_length,
            max_length=max_length,
            do_sample=False
        )

        return summary[0]["summary_text"]


def main():
    print(Fore.CYAN + Style.BRIGHT + "\nLLM Text Summarization System\n")
    
    user_name = input("Enter your name: ").strip() or "User"
    print(Fore.GREEN + f"\nWelcome {user_name}")

    print("\nEnter text to summarize: ")
    text = input("> ").strip()

    if not text:
        print(Fore.RED + "No input provided. Exiting.")
        return
    
    print(Fore.BLUE + "\nInitializing BART model...")
    engine = BarTextSummarizer()

    print(Fore.BLUE + "Performing summarization...")
    summary = engine.summarize(text)

    print(Fore.GREEN + Style.BRIGHT + f"Summary output for {user_name}: \n")
    print(summary)


if __name__ == "__main__":
    main()