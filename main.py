from groq import generate_response

def run_activity():
    print("ZERO-SHOT, ONE-SHOT AND FEW-SHOT ACTIVITY")

    category = input("Enter a category(e.g, animal, food, city): ").strip()
    item = input(f"Enter a specific {category} to classify:").strip()

    if not category or not item:
        print("Please fill in both feilds to run the activity.")
        return
    
    zero_shot = f"Is {item} a {category}? Answer yes or no."
    print("\n---ZERO-SHOT LEARNING---")
    print(f"Response: {generate_response(zero_shot, temperature=0.3, max_tokens=1024)}")

    one_shot = f"""Example:
Category: Fruit
Item: Apple
Answer: Yes. Apple is a fruit.

Now you try:
Category: {category}
Item: {item}
Answer:"""
    print("\n---ONE-SHOT LEARNING---")
    print(f"Response: {generate_response(one_shot, temperature=0.3, max_tokens=1024)}")

    few_shot = f"""Example 1:
Category: Fruit
Item: Apple
Answer: Yes. Apple is a fruit.

Now you try:
Category: {category}
Item: {item}
Answer:"""
    print("\n---FEW-SHOT LEARNING---")
    print(f"Response: {generate_response(few_shot, temperature=0.3, max_tokens=1024)}")
    
    creative_prompt = f"""Write one-sentence story about the given word.

Example 1: Word: moon
Story: The moon winked at the lovers as they shared their first kiss.

Word: {item}
Story:"""
    print("\n---CREATIVE FEW-SHOT EXAMPLE---")
    print(f"Response: {generate_response(creative_prompt, temperature=0.7, max_tokens=1024)}")

    print("\n---REFLECTION QUESTIONS---")
    print("1. How did the responses differ between zero-shot, ne-shot, and few-shot?")
    print("2. Which approach give the most helpful response?")
    print("3. How did the examples influence the model's output?")

if __name__  == "__main__":
    run_activity()