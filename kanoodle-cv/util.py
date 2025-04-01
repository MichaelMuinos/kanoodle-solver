from enum import Enum

import numpy as np
import json
import cv2

ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

def calculate_center(i, j):
    return (j * CIRCLE_INCREMENT + OFFSET_LEFT, i * CIRCLE_INCREMENT + OFFSET_TOP)

def draw_board(img):
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cv2.circle(img, calculate_center(i, j), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

def crop_circle(img, i, j):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)  # Empty black mask
    cv2.circle(mask, calculate_center(i, j), CIRCLE_RADIUS, CIRCLE_COLOR, -1)  # Fill in white circle
    result = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(mask)
    return result[y : y + h, x : x + w]
