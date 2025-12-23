import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.7, maxHands=1)

image_dir = "images"
os.makedirs(image_dir, exist_ok=True)

existing_files = [f for f in os.listdir(image_dir) if f.startswith("IMG_")]
serial = len(existing_files) + 1

palm_opened = False
capture_pending = False
capture_time = 0

while True:
    success, frame = cap.read()
    if not success:
        break

    hands, frame = detector.findHands(frame, draw=True)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        if fingers.count(1) >= 4 and not palm_opened:
            palm_opened = True

        if fingers.count(1) == 0 and palm_opened and capture_pending:
            capture_pending = True
            capture_time = time.time() + 3

    if capture_pending:
       remaining = int(capture_time - time.time())
       if remaining <= 0:
           file_name = f"IMG{serial}.jpg"
           cv2.imwrite(os.path.join(image_dir, file_name), frame)
           serial += 1
           capture_pending = False
           palm_opened = False
       else:
           cv2.putText(
               frame,
               f"Capturing in {remaining}",
               (30, 60),
               cv2.FONT_HERSHEY_SIMPLEX,
               1,
               (0, 0, 255),
               2
           )

    cv2.imshow("Gesture controlled camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()