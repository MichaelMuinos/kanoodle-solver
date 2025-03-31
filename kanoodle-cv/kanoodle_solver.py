from tuner.util import *

import numpy as np
import subprocess
import os
import cv2
import json
import argparse

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
DELIMETER = ","
COLOR_PATH = "bgr_colors.json"
ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

def get_letter(v, v2, v3, colors, color_detection):
    def _is_valid(v, v2, v3, values):
        return v >= values[0][0] and v <= values[0][1] and \
               v2 >= values[1][0] and v2 <= values[1][1] and \
               v3 >= values[2][0] and v3 <= values[2][1]

    for letter in colors:
        values = colors[letter][color_detection.name]
        if (_is_valid(v, v2, v3, values)):
            return letter

    # If no piece matches, consider it an empty space
    return '-'

def build_command(image):
    args = f"-m normal -i {image}"
    return f"./gradlew run --args=\'{args}\'"

def solve_config():
    cwd = f"{os.getcwd()}/kanoodle-algorithm"
    result = subprocess.run(build_command(), shell=True, capture_output=True, text=True, cwd=cwd)
    solved_config = result.stdout.split(NORMAL_MODE_PREFIX)[1].strip()
    print(solved_config)

def determine_letter(img, values, color_detection):
    v, v2, v3 = split_image(img)
    print(v, v2, v3)
    letter = get_letter(v, v2, v3, values, color_detection)
    print(letter)
    return letter

def read_tuned_colors():
    with open("tuner/" + COLOR_OUTPUT, 'r') as file:
        data = json.load(file)
        return data
    
def is_mostly_red(image, threshold=0.5):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for red color in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for the two red ranges
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    full_mask = cv2.bitwise_or(mask1, mask2)

    # Calculate the percentage of red pixels
    total_pixels = full_mask.shape[0] * full_mask.shape[1]
    red_pixels = cv2.countNonZero(full_mask)
    red_percentage = red_pixels / total_pixels

    return red_percentage > threshold

def build_config(img, color_detection):
    config = ""
    values = read_tuned_colors()
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cropped_img = crop_circle(img.copy(), i, j, color_detection)
            config += determine_letter(cropped_img, values, color_detection)
            cv2.imshow("test", cropped_img)
            cv2.waitKey(0)

        if i != ROWS:
            config += DELIMETER
    
    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bgr", help="will use BGR color detection if supplied, the default is HSV",
                        action="store_true")
    args = parser.parse_args()

    # Open default camera
    cap = cv2.VideoCapture(0)

    # Continuously show frames from the camera until the 'q' button is pressed
    img = None
    while True:
        _, board_img = cap.read()

        # Draw our board in the frame
        draw_board(board_img)

        # Display the frame
        cv2.imshow("board", board_img)

        # Hit 'q' to process the frame and solve the configuration
        if cv2.waitKey(1) == ord('q'):
            img = board_img.copy()
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

    print("Processing config...")
    color_detection = COLOR_DETECTION.BGR if args.bgr else COLOR_DETECTION.HSV
    config = build_config(img, color_detection)
    print(config)
