import numpy as np

import subprocess
import os
import cv2
import json

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
DELIMETER = ","
COLOR_PATH = "colors.json"
ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

def get_piece_letter(r, g, b, values):
    def _is_valid(r, g, b, v):
        return r >= v[0][0] and r <= v[0][1] and g >= v[1][0] and g <= v[1][1] and b >= v[2][0] and b <= v[2][1]

    for letter in values:
        v = values[letter]
        if (_is_valid(r, g, b, v)):
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

def determine_letter(img, values):
    r, g, b = cv2.split(img)
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
    print(int(r_avg), int(g_avg), int(b_avg))
    letter = get_piece_letter(int(r_avg), int(g_avg), int(b_avg), values)
    print(letter)
    return letter

def read_colors():
    with open(COLOR_PATH, 'r') as file:
        data = json.load(file)
        return data

def build_config(img):
    config = ""
    values = read_colors()
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cropped_img = crop_circle(img.copy(), i, j)
            config += determine_letter(cropped_img, values)
            cv2.imshow("test", cropped_img)
            cv2.waitKey(0)

        if i != ROWS:
            config += DELIMETER
    
    return config

if __name__ == "__main__":
    # Open default camera
    cap = cv2.VideoCapture(0)

    # Get default frame width + height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Continuously show frames from the camera until the 'q' button is pressed
    img = None
    while True:
        ret, board_img = cap.read()

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
    config = build_config(img)
    print(config)
