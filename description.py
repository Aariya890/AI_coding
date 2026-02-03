import os
from datetime import datetime
from PIL import Image
import torch
from transformers import (
    VisionEncoderDecoderModel,
    AutoImageProcessor,
    AutoTokenizer
)

MODEL_ID = "nlpconnect/vit-gpt2-image-captioning"


def ask_image():
    while True:
        path = input("Image path: ").strip().strip('"').strip("'")
        if os.path.isfile(path):
            return path
        print("File not found.")


def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID)
    processor = AutoImageProcessor.from_pretrained(MODEL_ID)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    model.to(device)
    model.eval()

    return model, processor, tokenizer, device


def generate_caption(image_path, model, processor, tokenizer, device):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    pixel_values = inputs.pixel_values.to(device)

    with torch.no_grad():
        output_ids = model.generate(
            pixel_values,
            max_length=60,
            num_beams=4,
            early_stopping=True
        )

    caption = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return caption


def save_caption(caption, image_path):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(image_path))[0]
    filename = f"{base}_caption_{ts}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(caption)

    print(f"Saved: {filename}")


def main():
    image_path = ask_image()

    print("Loading model...")
    model, processor, tokenizer, device = load_model()

    print("Generating description...")
    caption = generate_caption(image_path, model, processor, tokenizer, device)

    print("\nImage Description:")
    print(caption)

    if input("Save to text file? (y/n): ").lower() == "y":
        save_caption(caption, image_path)


if __name__ == "__main__":
    main()
