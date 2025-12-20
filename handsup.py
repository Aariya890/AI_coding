import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.7, maxHands=1)

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]

        fingers = detector.fingersUp(hand)

        cv2.putText(
            img,  f"Fingers: {fingers}",  (20, 50),   cv2.FONT_HERSHEY_SIMPLEX,  1,  (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()