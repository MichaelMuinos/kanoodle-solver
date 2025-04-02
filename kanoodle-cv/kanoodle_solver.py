from util import *

import numpy as np
import subprocess
import os
import cv2
import json
import argparse

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
TRACKBAR_COLOR_FILE = "trackbar_colors.json"
NO_ANSWER = "No valid answer."
DELIMETER = ","
EMPTY_SPACE = "-"
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

    cwd = f"{os.getcwd()}/../kanoodle-algorithm"
    result = subprocess.run(_build_command(img), shell=True, capture_output=True, text=True, cwd=cwd)
    return result.stdout.split(NORMAL_MODE_PREFIX)[1].strip()

def get_letter(img, colors, debug):
    def _calculate_letter_percentage(img, letter, lower_range, upper_range, debug):
        mask = cv2.inRange(img, np.array(lower_range), np.array(upper_range))

        # Calculate the percentage of matching pixels
        total_pixels = mask.shape[0] * mask.shape[1]
        matching_pixels = np.sum(mask > 0)
        percentage = matching_pixels / total_pixels
        if debug:
            print("Calculated Percentage: ", percentage)

        # Determine the appropriate threshold and return. The white piece is extremely accurate
        # typically, so a separate threshold can be used for that specific piece. This will allow
        # for the program to distinguish between gray, white, and light pink more easily.
        threshold = WHITE_THRESHOLD if letter == WHITE_PIECE else COMMON_THRESHOLD
        return percentage if percentage > threshold else 0

    max_percentage = 0
    max_letter = '-'
    for letter in colors:
        if debug:
            print("Checking Letter: ", letter)

        values = colors[letter]
        percentage = _calculate_letter_percentage(img.copy(), letter, values[0], values[1], debug)
        if (percentage > max_percentage):
            max_percentage = percentage
            max_letter = letter

    if debug:
        print("Chosen Letter: ", max_letter)

    return max_letter

def read_trackbar_colors():
        with open("trackbar/" + TRACKBAR_COLOR_FILE, 'r') as file:
            data = json.load(file)
            return data

def build_config(img, values, debug):
    config = ""
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cropped_img = crop_circle(img, i, j)
            config += get_letter(cropped_img, values, debug)
            # For debug mode we want to convert the cropped image back to BGR to
            # know what colored ball it is.
            if debug:
                cv2.imshow("cropped_img", cv2.cvtColor(cropped_img, cv2.COLOR_HSV2BGR))
                cv2.waitKey(0)

        if i != ROWS:
            config += DELIMETER
    
    return config

def draw_solution(img, original_config, solved_config, values):
    def _draw_x(img):
        # Calculate the center of the image
        height, width = img.shape[:2]
        center = (width // 2, height // 2)

        # Draw the 'x' at the center
        cv2.drawMarker(img, center, color=[0, 0, 255], thickness=10, markerType=cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA, markerSize=100)

    def _draw_filled_circle(img, i, j, hsv_values):
        # Take the middle HSV values and convert them to BGR.
        def _hsv_to_bgr_color(hsv_values):
            h = int((hsv_values[0][0] + hsv_values[1][0]) / 2)
            s = int((hsv_values[0][1] + hsv_values[1][1]) / 2)
            v = int((hsv_values[0][2] + hsv_values[1][2]) / 2)
            hsv_color = np.uint8([[[h, s, v]]])
            bgr_img = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
            return (int(bgr_img[0][0][0]), int(bgr_img[0][0][1]), int(bgr_img[0][0][2]))

        bgr_color = _hsv_to_bgr_color(hsv_values)
        cv2.circle(solution_board, calculate_center(i, j), CIRCLE_RADIUS, bgr_color, -1)

    solution_board = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    if solved_config == NO_ANSWER:
        # Draw an 'x' indicating that no solution was found
        _draw_x(solution_board)
    else:
        original_rows = original_config.split(DELIMETER)
        solved_rows = solved_config.split(DELIMETER)
        for i in range(1, ROWS + 1):
            for j in range(1, COLS + 1):
                # Only draw a circle for an empty space (i.e. '-')
                if original_rows[i - 1][j - 1] == EMPTY_SPACE:
                    hsv_values = values[solved_rows[i - 1][j - 1]]
                    _draw_filled_circle(solution_board, i, j, hsv_values)

    cv2.imshow("Solution: ", solution_board)
    cv2.waitKey(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="run in debug mode",
                        action="store_true")
    args = parser.parse_args()

    # Open default camera
    cap = cv2.VideoCapture(0)

    # Read trackbar colors
    values = read_trackbar_colors()

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
            cv2.imwrite("example-config-3.png", board)
            board = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

    print("Processing config...")
    config = build_config(board, values, args.debug)

    print("Solving config...")
    solved_config = solve_config(config)

    print("Done.")
    draw_solution(board, config, solved_config, values)
