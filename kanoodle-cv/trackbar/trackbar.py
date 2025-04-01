import cv2
import numpy as np
import argparse
import json

WINDOW_NAME = "board"
LETTERS = "ABCDEFGHIJKL"
 
def get_hsv_trackbar_positions():
    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('HMin', WINDOW_NAME)
    s_min = cv2.getTrackbarPos('SMin', WINDOW_NAME)
    v_min = cv2.getTrackbarPos('VMin', WINDOW_NAME)
    h_max = cv2.getTrackbarPos('HMax', WINDOW_NAME)
    s_max = cv2.getTrackbarPos('SMax', WINDOW_NAME)
    v_max = cv2.getTrackbarPos('VMax', WINDOW_NAME)
    return [[h_min, s_min, v_min], [h_max, s_max, v_max]]

def nothing(unused):
    pass

def save_callback(value, colors):
    if value == 1:
        letter_index = cv2.getTrackbarPos('Letter', WINDOW_NAME)
        letter = LETTERS[letter_index]

        print("Saving letter ", letter, "...")

        hsv_positions = get_hsv_trackbar_positions()
        colors[letter] = hsv_positions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="name of the image",
                        type=str, default="example-full-board.png")
    args = parser.parse_args()

    # Build our letter to color mapping
    colors = {}

    # Load image
    image = cv2.imread("trackbar/" + args.image)

    # Create a WINDOW_NAME
    cv2.namedWindow(WINDOW_NAME)

    # Create trackbars for color change
    # Hue is from 0-179 for Opencv
    cv2.createTrackbar('HMin', WINDOW_NAME, 0, 179, nothing)
    cv2.createTrackbar('SMin', WINDOW_NAME, 0, 255, nothing)
    cv2.createTrackbar('VMin', WINDOW_NAME, 0, 255, nothing)
    cv2.createTrackbar('HMax', WINDOW_NAME, 0, 179, nothing)
    cv2.createTrackbar('SMax', WINDOW_NAME, 0, 255, nothing)
    cv2.createTrackbar('VMax', WINDOW_NAME, 0, 255, nothing)

    # Create a mock button to save the values for a specific letter
    cv2.createTrackbar('Save', WINDOW_NAME, 0, 1, lambda x : save_callback(x, colors))

    # Create trackbar to represent a letter (indices 0 to 11)
    cv2.createTrackbar('Letter', WINDOW_NAME, 0, 11, nothing)

    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMax', WINDOW_NAME, 179)
    cv2.setTrackbarPos('SMax', WINDOW_NAME, 255)
    cv2.setTrackbarPos('VMax', WINDOW_NAME, 255)

    while True:
        # Get current positions of all trackbars
        hsv_positions = get_hsv_trackbar_positions()

        # Set minimum and maximum HSV values to display
        lower = np.array(hsv_positions[0])
        upper = np.array(hsv_positions[1])

        # Convert to HSV format and color threshold
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        # Display result image
        cv2.imshow('image', result)

        # Hit 'q' to exit
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

    print(colors)