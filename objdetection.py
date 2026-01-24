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

def draw_boxes(image, detection, threshold=0.5):
    draw = ImageDraw.Draw(image)
    font = load_font()
    summary = {}

    for det in detections:
        score = float(det.get("score"), 0)
        if score < threshold:
            continue

        label = det.get("image", "object")
        