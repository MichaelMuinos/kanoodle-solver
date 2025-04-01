from util import *

import numpy as np
import json
import cv2
import argparse

PRESET_CONFIG = "EEGGGJJJJIIAEEEGCDDDDIAAALGCHHDIIBBLLLCFHHKKBBBLCCFFHKK"
    
def calculate_optimal_colors(bgr_img, hsv_img, colors):
    def _update_colors(bgr_img, hsv_img, letter, colors):
        def _helper(img, color_detection, letter, colors):
            v, v2, v3 = split_image(img)
            if len(colors[letter][color_detection.name]) == 0:
                colors[letter][color_detection.name] = [[v, v2, v3], [v, v2, v3]]
            else:
                values = colors[letter][color_detection.name]
                values[0][0] = min(values[0][0], v)
                values[0][1] = min(values[0][1], v2)
                values[0][2] = min(values[0][2], v3)
                values[1][0] = max(values[1][0], v)
                values[1][1] = max(values[1][1], v2)
                values[1][2] = max(values[1][2], v3)

        if letter not in colors:
            colors[letter] = {
                COLOR_DETECTION.BGR.name: [],
                COLOR_DETECTION.HSV.name: []
            }

        _helper(bgr_img, COLOR_DETECTION.BGR, letter, colors)
        _helper(hsv_img, COLOR_DETECTION.HSV, letter, colors)

    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            index = (i - 1) * COLS + (j - 1)
            letter = PRESET_CONFIG[index]
            bgr_cropped_img = crop_circle(bgr_img, i, j)
            hsv_cropped_img = crop_circle(hsv_img, i, j)
            _update_colors(bgr_cropped_img, hsv_cropped_img, letter, colors)

def write_to_file(colors):
    with open(COLOR_OUTPUT, 'w') as file:
        json.dump(colors, file, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", help="determines if we will write the color boundaries to a file",
                        action="store_true")
    parser.add_argument("--repeat", help="determines if we will continue to process images without constant button pressing",
                        action="store_true")
    args = parser.parse_args()

    # Open default camera
    cap = cv2.VideoCapture(0)

    colors = {}
    c_pressed = False
    while True:
        _, board_img = cap.read()

        # Draw our board in the frame
        draw_board(board_img)

        # Display the frame
        cv2.imshow("board", board_img)

        pressed_key = cv2.waitKey(1) & 0xFF
        if pressed_key == ord('c') or (args.repeat and c_pressed):
            print("Calculating colors...")
            c_pressed = True
            bgr_img = board_img.copy()
            hsv_img = cv2.cvtColor(board_img.copy(), cv2.COLOR_BGR2HSV)
            calculate_optimal_colors(bgr_img, hsv_img, colors)

        if pressed_key == ord('q'):
            print("Stopping camera...")
            break

    # Release the camera and close the windows
    cap.release()
    cv2.destroyAllWindows()

    # Either write or print
    if args.write:
        print("Writing colors to file...")
        write_to_file(colors)
    else:
        print("Printing colors...")
        print(colors)
