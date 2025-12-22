import cv2
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(detectionCon=0.8, maxHands=1)

score = 0
target_x = random.randint(50, 590)
target_y = random.randint(50, 430)
radius = 25

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    cv2.circle(img, (target_x, target_y), radius, (0, 0, 255), -1)

    if hands:
        lmList = hands[0]["lmList"]

        ix, iy = lmList[8][0], lmList[8][1]

        cv2.circle(img, (ix, iy), 15, (255, 0, 0), -1)

        dist = ((ix - target_x)**2 + (iy - target_y)**2) ** 0.5
        if dist < radius + 15:
            score += 1
            target_x = random.randint(50, 590)
            target_y = random.randint(50, 430)

    cv2.putText(img, f"Score: {score}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Game", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
