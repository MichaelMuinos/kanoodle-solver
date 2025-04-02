from util import *

import numpy as np
import subprocess
import os
import cv2
import json
import argparse

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
TRACKBAR_COLOR_FILE = "trackbar_colors.json"
DELIMETER = ","
# All colors other than white
COMMON_THRESHOLD = 0.25
# It is really hard to distinguish gray / light pink / white. Let's set
# a really high white threshold to tell them apart.
WHITE_PIECE = "F"
WHITE_THRESHOLD = 0.7

def solve_config(img):
    def _build_command(img):
        args = f"-m normal -i {img}"
        return f"./gradlew run --args=\'{args}\'"

    cwd = f"{os.getcwd()}/kanoodle-algorithm"
    result = subprocess.run(build_command(), shell=True, capture_output=True, text=True, cwd=cwd)
    solved_config = result.stdout.split(NORMAL_MODE_PREFIX)[1].strip()
    print(solved_config)

def get_letter(img, colors):
    def _calculate_letter_percentage(img, letter, lower_range, upper_range):
        mask = cv2.inRange(img, np.array(lower_range), np.array(upper_range))

        # Calculate the percentage of matching pixels
        total_pixels = mask.shape[0] * mask.shape[1]
        matching_pixels = np.sum(mask > 0)
        percentage = matching_pixels / total_pixels

        # Determine the appropriate threshold and return
        threshold = WHITE_THRESHOLD if letter == WHITE_PIECE else COMMON_THRESHOLD
        return percentage if percentage > threshold else 0

    max_percentage = 0
    max_letter = '-'
    for letter in colors:
        values = colors[letter]
        percentage = _calculate_letter_percentage(img.copy(), letter, values[0], values[1])
        if (percentage > max_percentage):
            max_percentage = percentage
            max_letter = letter

    return max_letter

def build_config(img):
    def _read_trackbar_colors():
        with open("trackbar/" + TRACKBAR_COLOR_FILE, 'r') as file:
            data = json.load(file)
            return data

    config = ""
    values = _read_trackbar_colors()
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cropped_img = crop_circle(img, i, j)
            config += get_letter(cropped_img, values)

        if i != ROWS:
            config += DELIMETER
    
    return config

if __name__ == "__main__":
    # Open default camera
    cap = cv2.VideoCapture(0)

    # Continuously show frames from the camera until the 'q' button is pressed
    board = None
    while True:
        _, board = cap.read()

        # Copy the board to draw on
        modified_board = board.copy()

        # Draw our board in the frame
        draw_board(modified_board)

        # Display the frame
        cv2.imshow("board", modified_board)

        # Hit 'q' to process the frame and solve the configuration
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite("img2.png", board)
            board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

    print("Processing config...")
    config = build_config(board)
    print(config)
