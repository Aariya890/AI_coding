import cv2
import mediapipe as mp
import pyautogui
import math
import time

screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smoothening = 5

click_delay = 0.4
last_click_time = 0

dragging = False
pinch_start_time = 0
pinching = False

mode_active = True

last_scroll_time = 0
scroll_delay = 0.4

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    return [lm[tip].y < lm[tip - 2].y for tip in tips]

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (380, 200), (20, 20, 20), -1)
    frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)

    cv2.putText(frame, f"MODE: {'ACTIVE' if mode_active else 'PAUSED'}",
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 0) if mode_active else (0, 0, 255), 2)

    cv2.putText(frame, "Thumb+Index = LEFT CLICK", (10, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.putText(frame, "Thumb+Middle = RIGHT CLICK", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    cv2.putText(frame, "Hold Thumb+Index = DRAG", (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

    cv2.putText(frame, "Index+Middle UP = SCROLL UP", (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    cv2.putText(frame, "FIST = SCROLL DOWN", (10, 155),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.putText(frame, "M = Toggle Mode | Q = Quit", (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index = lm[8]
            middle = lm[12]
            thumb = lm[4]

            x = int(index.x * screen_w)
            y = int(index.y * screen_h)

            curr_x = prev_x + (x - prev_x) / smoothening
            curr_y = prev_y + (y - prev_y) / smoothening

            if mode_active:
                pyautogui.moveTo(curr_x, curr_y)

            prev_x, prev_y = curr_x, curr_y

            cv2.circle(frame, (int(index.x * w), int(index.y * h)), 10, (0, 255, 0), -1)
            cv2.circle(frame, (int(middle.x * w), int(middle.y * h)), 10, (255, 0, 0), -1)
            cv2.circle(frame, (int(thumb.x * w), int(thumb.y * h)), 10, (0, 165, 255), -1)

            dist_thumb_index = distance(index, thumb)
            dist_thumb_middle = distance(middle, thumb)

            fingers = fingers_up(lm)
            now = time.time()

            if mode_active:

                if dist_thumb_index < 0.04:
                    if not pinching:
                        pinch_start_time = now
                        pinching = True
                    elif not dragging and (now - pinch_start_time > 0.5):
                        pyautogui.mouseDown()
                        dragging = True
                else:
                    if pinching:
                        duration = now - pinch_start_time
                        if duration < 0.3 and (now - last_click_time > click_delay):
                            pyautogui.click()
                            last_click_time = now
                        if dragging:
                            pyautogui.mouseUp()
                            dragging = False
                    pinching = False

                if dist_thumb_middle < 0.04 and (now - last_click_time > click_delay):
                    pyautogui.rightClick()
                    last_click_time = now

                index_up, middle_up, ring_up, pinky_up = fingers

                scroll_up = index_up and middle_up and not ring_up and not pinky_up
                scroll_down = not index_up and not middle_up and not ring_up and not pinky_up

                if now - last_scroll_time > scroll_delay:
                    if scroll_up:
                        pyautogui.scroll(50)
                        last_scroll_time = now

                    elif scroll_down:
                        pyautogui.scroll(-50)
                        last_scroll_time = now

    cv2.imshow("Gesture Mouse Pro", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break
    elif key == ord("m"):
        mode_active = not mode_active

cap.release()
cv2.destroyAllWindows()