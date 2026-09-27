from __future__ import annotations
import cv2
import numpy as np
import time
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from gesture_detector   import GestureDetector
from gesture_classifier import classify
from controller         import GestureController

GESTURE_COLOR = {
    "point":      (  0, 255,   0),
    "pinch":      (  0, 200, 255),
    "two_up":     (255, 180,   0),
    "fist":       (  0,   0, 255),
    "open_palm":  (200, 200, 200),
    "thumb_up":   (  0, 255, 128),
    "thumb_down": (  0, 128, 255),
    "l_shape":    (255, 255,   0),
    "three_up":   (255,   0, 255),
    "four_up":    (128,   0, 255),
    "none":       ( 80,  80,  80),
}

def draw_hud(frame, gesture, action, fps, paused):
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 56), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    color = GESTURE_COLOR.get(gesture, (255, 255, 255))
    cv2.putText(frame, f"Gesture: {gesture}", (16, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2, cv2.LINE_AA)
    cv2.putText(frame, action, (w // 2 - 160, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 1, cv2.LINE_AA)
    fps_txt = f"FPS {fps:4.1f}" if not paused else "PAUSED"
    cv2.putText(frame, fps_txt, (w - 160, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (160, 160, 160), 1, cv2.LINE_AA)
    legend = [
        ("point",      "move cursor"),
        ("pinch",      "left click"),
        ("two_up",     "scroll"),
        ("fist",       "right click"),
        ("open_palm",  "neutral/stop"),
        ("thumb_up",   "volume up"),
        ("thumb_down", "volume down"),
        ("l_shape",    "brightness up"),
        ("three_up",   "screenshot"),
        ("four_up",    "play/pause"),
    ]
    for i, (g, desc) in enumerate(legend):
        y = h - 20 - i * 22
        c = GESTURE_COLOR.get(g, (200, 200, 200))
        cv2.putText(frame, f"{g:<12} {desc}", (16, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, 1, cv2.LINE_AA)
    return frame

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    detector   = GestureDetector(max_hands=1)
    controller = GestureController()
    paused  = False
    gesture = "none"
    action  = ""
    fps     = 0.0
    t_prev  = time.perf_counter()
    print("GestureControls started. Press Q to quit, P to pause.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Cannot read from camera.")
            break
        t_now = time.perf_counter()
        fps   = 0.9 * fps + 0.1 * (1.0 / max(t_now - t_prev, 1e-6))
        t_prev = t_now
        hands, annotated = detector.process(frame)
        if not paused and hands:
            hand    = hands[0]
            gesture = classify(hand.landmarks)
            action  = controller.handle(gesture, hand.landmarks)
        elif not hands:
            gesture = "none"
            action  = ""
        annotated = draw_hud(annotated, gesture, action, fps, paused)
        cv2.imshow("GestureControls", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("p"):
            paused = not paused
    cap.release()
    detector.close()
    cv2.destroyAllWindows()
    print("GestureControls closed.")

if __name__ == "__main__":
    main()
