import numpy as np

import json
import cv2
import argparse

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
DELIMETER = ","
PRESET_CONFIG = "EEGGGJJJJIIAEEEGCDDDDIAAALGCHHDIIBBLLLCFHHKKBBBLCCFFHKK"
ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
RGB_ADJUSTMENT = 2
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

def update_values(img, letter, values):
    r, g, b = cv2.split(img)
    r_avg = int(cv2.mean(r)[0])
    g_avg = int(cv2.mean(g)[0])
    b_avg = int(cv2.mean(b)[0])
    if letter in values:
        values[letter][0][0] = min(values[letter][0][0], r_avg)
        values[letter][0][1] = max(values[letter][0][1], r_avg)
        values[letter][1][0] = min(values[letter][1][0], g_avg)
        values[letter][1][1] = max(values[letter][1][1], g_avg)
        values[letter][2][0] = min(values[letter][2][0], b_avg)
        values[letter][2][1] = max(values[letter][2][1], b_avg)
    else:
        values[letter] = [[r_avg, r_avg], [g_avg, g_avg], [b_avg, b_avg]]

    
def calculate_optimal_colors(img, values):
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            index = (i - 1) * COLS + (j - 1)
            letter = PRESET_CONFIG[index]
            cropped_img = crop_circle(img.copy(), i, j)
            update_values(cropped_img, letter, values)

def apply_rgb_adjustment(values):
    # Apply a slight adjustment for each letter to make sure we capture the correct letter
    for key in values:
        values[key][0][0] = max(values[key][0][0] - RGB_ADJUSTMENT, 0)
        values[key][0][1] = min(values[key][0][1] + RGB_ADJUSTMENT, 255)
        values[key][1][0] = max(values[key][1][0] - RGB_ADJUSTMENT, 0)
        values[key][1][1] = min(values[key][1][1] + RGB_ADJUSTMENT, 255)
        values[key][2][0] = max(values[key][2][0] - RGB_ADJUSTMENT, 0)
        values[key][2][1] = min(values[key][2][1] + RGB_ADJUSTMENT, 255)

def write_to_file(values):
    apply_rgb_adjustment(values)
    with open('colors.json', 'w') as file:
        json.dump(values, file, indent=4)

if __name__ == "__main__":
    # Open default camera
    cap = cv2.VideoCapture(0)

    # Get default frame width + height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    values = {}
    while True:
        ret, board_img = cap.read()

        # Draw our board in the frame
        draw_board(board_img)

        # Display the frame
        cv2.imshow("board", board_img)

        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('c'):
            print("Calculating values...")
            img = board_img.copy()
            calculate_optimal_colors(img, values)
        elif pressed_key == ord('q'):
            print("Stopping camera...")
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if args.write:
        write_to_file(values)
    else:
        print(values)
