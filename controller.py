from __future__ import annotations
import time
import pyautogui
import numpy as np
import keyboard
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from config import (
    SMOOTHING, SCROLL_SPEED, DEBOUNCE_FRAMES, EDGE_MARGIN,
    TRACK_REGION, INDEX_TIP,
)

pyautogui.FAILSAFE = False
pyautogui.PAUSE   = 0

class GestureController:
    def __init__(self):
        self._screen_w, self._screen_h = pyautogui.size()
        self._cur_x = self._screen_w  / 2
        self._cur_y = self._screen_h / 2
        self._last_gesture  = "none"
        self._gesture_count = 0
        self._scroll_base_y = None
        self._last_click_time = 0.0
        self._click_cooldown  = 0.5
        self._last_action_time = 0.0
        self._action_cooldown  = 1.0

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self._volume = cast(interface, POINTER(IAudioEndpointVolume))

    def handle(self, gesture, landmarks):
        if gesture == self._last_gesture:
            self._gesture_count += 1
        else:
            self._gesture_count = 1
            self._last_gesture  = gesture
        stable = self._gesture_count >= DEBOUNCE_FRAMES
        action = gesture

        if gesture == "point":
            action = self._move_cursor(landmarks)
        elif gesture == "pinch" and stable:
            action = self._left_click()
        elif gesture == "two_up":
            action = self._scroll(landmarks)
        elif gesture == "fist" and stable:
            action = self._right_click()
        elif gesture == "open_palm":
            action = "pause"
            self._scroll_base_y = None
        elif gesture == "thumb_up" and stable:
            action = self._volume_up()
        elif gesture == "thumb_down" and stable:
            action = self._volume_down()
        elif gesture == "l_shape" and stable:
            action = self._brightness_up()
        elif gesture == "three_up" and stable:
            action = self._screenshot()
        elif gesture == "four_up" and stable:
            action = self._media_playpause()

        return action

    def _norm_to_screen(self, nx, ny):
        tr = TRACK_REGION
        rx = (nx - tr["x_min"]) / (tr["x_max"] - tr["x_min"])
        ry = (ny - tr["y_min"]) / (tr["y_max"] - tr["y_min"])
        rx = max(0.0, min(1.0, rx))
        ry = max(0.0, min(1.0, ry))
        sx = rx * self._screen_w
        sy = ry * self._screen_h
        sx = max(EDGE_MARGIN, min(self._screen_w  - EDGE_MARGIN, sx))
        sy = max(EDGE_MARGIN, min(self._screen_h - EDGE_MARGIN, sy))
        return sx, sy

    def _move_cursor(self, landmarks):
        nx = 1.0 - landmarks[INDEX_TIP, 0]
        ny = landmarks[INDEX_TIP, 1]
        tx, ty = self._norm_to_screen(nx, ny)
        self._cur_x += SMOOTHING * (tx - self._cur_x)
        self._cur_y += SMOOTHING * (ty - self._cur_y)
        pyautogui.moveTo(int(self._cur_x), int(self._cur_y))
        return f"move ({int(self._cur_x)}, {int(self._cur_y)})"

    def _left_click(self):
        now = time.time()
        if now - self._last_click_time > self._click_cooldown:
            pyautogui.click()
            self._last_click_time = now
            return "left click"
        return "click cooldown"

    def _right_click(self):
        now = time.time()
        if now - self._last_click_time > self._click_cooldown:
            pyautogui.rightClick()
            self._last_click_time = now
            return "right click"
        return "rclick cooldown"

    def _scroll(self, landmarks):
        ny = landmarks[INDEX_TIP, 1]
        if self._scroll_base_y is None:
            self._scroll_base_y = ny
            return "scroll init"
        delta = ny - self._scroll_base_y
        direction = -1 if delta < 0 else 1
        pyautogui.scroll(direction * SCROLL_SPEED)
        return f"scroll {'up' if direction > 0 else 'down'}"

    def _volume_up(self):
        now = time.time()
        if now - self._last_action_time > self._action_cooldown:
            current = self._volume.GetMasterVolumeLevelScalar()
            self._volume.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
            self._last_action_time = now
            return "volume up"
        return "volume up (cooldown)"

    def _volume_down(self):
        now = time.time()
        if now - self._last_action_time > self._action_cooldown:
            current = self._volume.GetMasterVolumeLevelScalar()
            self._volume.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
            self._last_action_time = now
            return "volume down"
        return "volume down (cooldown)"

    def _brightness_up(self):
        now = time.time()
        if now - self._last_action_time > self._action_cooldown:
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(min(100, current + 10), display=0)
            self._last_action_time = now
            return "brightness up"
        return "brightness (cooldown)"

    def _screenshot(self):
        now = time.time()
        if now - self._last_action_time > self._action_cooldown:
            filename = f"screenshot_{int(time.time())}.png"
            pyautogui.screenshot(filename)
            self._last_action_time = now
            return "screenshot saved"
        return "screenshot (cooldown)"

    def _media_playpause(self):
        now = time.time()
        if now - self._last_action_time > self._action_cooldown:
            keyboard.send("play/pause media")
            self._last_action_time = now
            return "play/pause"
        return "media (cooldown)"
