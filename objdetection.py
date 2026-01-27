import os
import io
import time
import random
import base64
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import HF_API_KEY

MODEL = "facebook/detr-resnet-50"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"

ALLOWED = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}

def load_font(size=18):
    for name in ("DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except:
            pass
    return ImageFont.load_default()    

def ask_image():
    print("\nSAelect an image")
    while True:
        path = input("Image path: ").strip().strip('"').strip("'")
        if not os.path.isfile(path):
            print("File not found.")
            continue
        if os.path.splitext(path)[1].lower() not in ALLOWED:
            print("Unsupported format.")
            continue
        try:
            Image.open(path).verify
        except:
            print("Invalid image.")
            continue
        return path
    
def infer(image_bytes, retries=8):
    payload = {
        "inputs" : base64.b64encode(image_bytes).decode("utf-8")
    }

    headers = {
        "Authorization" : f"Bearer {HF_API_KEY}",
        "Content-Type" : "application/json"
    }

    for _ in range(retries):
        r = requests.post(API, headers=headers, json=payload, timeout=60)
        
        if r.status_code == 200:
            return r.json()
        
        if r.status_code == 503:
            time.sleep(2)
            continue

        raise RuntimeError(f"API {r.status_code} : {r.text[:200]}")
    
    raise RuntimeError(f"Inference warm-up timeout.")

def draw_boxes(image, detections, threshold=0.5):
    draw = ImageDraw.Draw(image)
    font = load_font()
    summary = {}

    for det in detections:
        score = float(det.get("score", 0))
        if score < threshold:
            continue

        label = det.get("label", "object")
        box = det.get("box", {})

        x1 = int(box.get("xmin", 0))
        y1 = int(box.get("ymin", 0))
        x2 = int(box.get("xmax", 0)) 
        y2 = int(box.get("ymax", 0))

        color = tuple(random.randint(80, 255) for _ in range(3))
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=4)

        text = f"{label} {int(score * 100)}%"
        tw = draw.textlength(text, font=font)
        th = font.size + 6

        draw.rectangle([(x1, y1 - th), (x1 + tw + 8, y1)], fill=color)
        draw.text((x1 + 4, y1 - th + 3), text, font=font, fill=(0, 0, 0))

        summary[label] = summary.get(label, 0) + 1

    return summary

def main():
    image_path = ask_image()

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    
    try:
        detections = infer(image_bytes)
    except Exception as e:
        print("Inference failed.", e)
        return
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    summary = draw_boxes(image, detections)

    output = f"annotated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image.save(output)

    print(f"\nAnnotated image saved: {output}")

    if summary:
        print("\nDetected objects:")
        for label, count in sorted(summary.items(), key=lambda x: -x[1]):
            print(f"{label} : {count}")
    else:
        print("No confident detections found.")

    print("\nDisclaimer: Results are AI-generated and may be imperfect.")

if __name__  == "__main__":
    main()