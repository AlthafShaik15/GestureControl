from __future__ import annotations
import cv2
import mediapipe as mp
import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass
class HandData:
    landmarks: np.ndarray
    handedness: str
    raw: object

class GestureDetector:
    def __init__(self, max_hands=1, detection_confidence=0.75, tracking_confidence=0.75):
        self._mp_hands = mp.solutions.hands
        self._mp_draw  = mp.solutions.drawing_utils
        self._mp_style = mp.solutions.drawing_styles
        self._hands = self._mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process(self, frame):
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)
        annotated = frame.copy()
        hands = []
        if results.multi_hand_landmarks:
            for idx, lm_list in enumerate(results.multi_hand_landmarks):
                self._mp_draw.draw_landmarks(
                    annotated, lm_list,
                    self._mp_hands.HAND_CONNECTIONS,
                    self._mp_style.get_default_hand_landmarks_style(),
                    self._mp_style.get_default_hand_connections_style(),
                )
                pts = np.array([[lm.x, lm.y, lm.z] for lm in lm_list.landmark], dtype=np.float32)
                handedness = results.multi_handedness[idx].classification[0].label
                hands.append(HandData(landmarks=pts, handedness=handedness, raw=lm_list))
        return hands, annotated

    def close(self):
        self._hands.close()
