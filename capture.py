import cv2
import os

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Failed to load camera.")
    exit()

folder = "images"
os.makedirs(folder, exist_ok=True)

existing = [f for f in os.listdir(folder) if f startswith("IMG_") and f endswith(".jpg")]
serial = len(existing) + 1

while True():
    ret, frame = cap.read()

    if not ret:
        print("ERROR: Failed to capture image!")
        break

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('s'):
        filename = f"IMG_{serial}.jpg"
        cv2.imwrite(os.path.join(folder, filename), frame)
        serial += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()