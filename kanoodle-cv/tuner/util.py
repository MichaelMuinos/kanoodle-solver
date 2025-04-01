from enum import Enum

import numpy as np
import json
import cv2

COLOR_OUTPUT = "trackbar_colors_output_5.json"
ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

class COLOR_DETECTION(Enum):
    BGR = 1
    HSV = 2

def calculate_center(i, j):
    return (j * CIRCLE_INCREMENT + OFFSET_LEFT, i * CIRCLE_INCREMENT + OFFSET_TOP)

def draw_board(img):
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cv2.circle(img, calculate_center(i, j), CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

def split_image(img):
    show(img)
    v, v2, v3 = cv2.split(img)
    v_avg = int(cv2.mean(v)[0])
    v2_avg = int(cv2.mean(v2)[0])
    v3_avg = int(cv2.mean(v3)[0])
    return v_avg, v2_avg, v3_avg

def crop_circle(img, i, j):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)  # Empty black mask
    cv2.circle(mask, calculate_center(i, j), CIRCLE_RADIUS, CIRCLE_COLOR, -1)  # Fill in white circle
    result = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(mask)
    return result[y : y + h, x : x + w]

def show(img):
    cv2.imshow("test", img)
    cv2.waitKey(0)