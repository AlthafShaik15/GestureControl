from __future__ import annotations
import numpy as np
from config import (
    PINCH_THRESHOLD, FIST_THRESHOLD,
    THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP,
    WRIST, INDEX_MCP, MIDDLE_MCP, RING_MCP, PINKY_MCP,
)

def _tip_above_mcp(lm, tip, mcp):
    return lm[tip, 1] < lm[mcp, 1]

def _dist(lm, a, b):
    return float(np.linalg.norm(lm[a, :2] - lm[b, :2]))

def classify(landmarks):
    lm = landmarks

    index_up  = _tip_above_mcp(lm, INDEX_TIP,  INDEX_MCP)
    middle_up = _tip_above_mcp(lm, MIDDLE_TIP, MIDDLE_MCP)
    ring_up   = _tip_above_mcp(lm, RING_TIP,   RING_MCP)
    pinky_up  = _tip_above_mcp(lm, PINKY_TIP,  PINKY_MCP)
    thumb_up  = lm[THUMB_TIP, 1] < lm[WRIST, 1] - 0.1

    thumb_right = lm[THUMB_TIP, 0] > lm[INDEX_MCP, 0]
    thumb_left  = lm[THUMB_TIP, 0] < lm[INDEX_MCP, 0]

    tips = [INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
    avg_dist = float(np.mean([_dist(lm, t, WRIST) for t in tips]))

    if index_up and middle_up and ring_up and pinky_up:
        return "open_palm"

    if avg_dist < FIST_THRESHOLD:
        return "fist"

    if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        if lm[THUMB_TIP, 1] < lm[WRIST, 1]:
            return "thumb_up"

    if not thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        if lm[THUMB_TIP, 1] > lm[WRIST, 1]:
            return "thumb_down"

    if index_up and not middle_up and not ring_up and not pinky_up:
        if _dist(lm, THUMB_TIP, INDEX_MCP) > 0.1:
            return "l_shape"

    if _dist(lm, THUMB_TIP, INDEX_TIP) < PINCH_THRESHOLD:
        return "pinch"

    if index_up and middle_up and ring_up and not pinky_up:
        return "three_up"

    if index_up and middle_up and ring_up and pinky_up:
        return "four_up"

    if index_up and middle_up and not ring_up and not pinky_up:
        return "two_up"

    if index_up and not middle_up and not ring_up and not pinky_up:
        return "point"

    return "none"
