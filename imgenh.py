import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from datetime import datetime
from config import HF_API_KEY

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate(prompt: str) -> Image.Image:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Accept": "image/png"
    }
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    if response.status_code != 200:
        try:
            error_data = response.json()
            raise Exception(error_data.get("error", "Unknown API error"))
        except ValueError:
            raise Exception(response.text)
        
    return Image.open(BytesIO(response.content))

def post_process_image(image: Image.Image, brightness_pct: float, contrast_pct: float, blur_pct: float) -> Image.Image:

    brightness_factor = 1 + (brightness_pct / 100)
    contrast_factor = 1 + (contrast_pct / 100)
    blur_radius = blur_pct / 100

    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    image = ImageEnhance.Contrast(image).enhance(contrast_factor)
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    return image

def save_images(original: Image.Image, processed: Image.Image) -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file = f"IMG_{timestamp}_original.png"
    processed_file = f"IMG_{timestamp}_processed.png"

    original.save(original_file)
    processed.save(processed_file)

    return original_file, processed_file

def main():
    print("Text-to-text image Generator with Adjustable post-processing")
    print("Type 'exit' to quit.\n" )

while True:
    prompt = input("Enter image description: \n").strip()
    if prompt.lower() == "exit":
        print("Session terminated.")
        break

    try:
        brightness_pct = float(input("Enter brightness adjustment (%): ").strip())
        contrast_pct = float(input("Enter contrast adjustment (%): ").strip())
        blur_pct = float(input("Enter blur amount (%): ").strip())

        if not (0 <= blur_pct <= 100):
            raise ValueError("Blur must be between 0 to 100%.")
        
        print("\nGenerating Image...\n")
        image = generate(prompt)
        processed_image = post_process_image(image, brightness_pct, contrast_pct, blur_pct)

        original_file, processed_file = save_images(image, processed_image)
        print(f"Original file saved as: {original_file}")
        print(f"Processed file saved as: {processed_file}\n")

    except ValueError as ve:
        print(f"Input error: {ve}\n")    
    except Exception as e:
        print(f"Operational error: {e}\n")     

if __name__ == "__main__":
    main()           