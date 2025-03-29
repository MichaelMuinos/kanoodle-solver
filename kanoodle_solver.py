import numpy as np

import subprocess
import os
import cv2

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
ROWS = 5
COLS = 11
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

def get_piece_letter(r, g, b):
    # A = ORANGE
    if (r >= 204 and r <= 255) and (g >= 40 and g <= 178) and (b >= 0 and b <= 102):
        return 'A'
    
    # B = RED
    if (r >= 135 and r <= 255) and (g >= 0 and g <= 51) and (b >= 0 and b <= 51):
        return 'B'
    
    # C = DARK BLUE
    if (r >= 0 and r <= 51) and (g >= 0 and g <= 100) and (b >= 116 and b <= 255):
        return 'C'
    
    # D = LIGHT PINK
    if (r >= 165 and r <= 255) and (g >= 110 and g <= 255) and (b >= 140 and b <= 255):
        return 'D'
    
    # E = DARK GREEN
    if (r >= 0 and r <= 30) and (g >= 70 and g <= 103) and (b >= 60 and b <= 103):
        return 'E'
    
    # F = WHITE
    if (r >= 165 and r <= 255) and (g >= 190 and g <= 255) and (b >= 190 and b <= 255):
        return 'F'
    
    # G = LIGHT BLUE
    if (r >= 50 and r <= 80) and (g >= 135 and g <= 200) and (b >= 160 and b <= 210):
        return 'G'
    
    # H = DARK PINK
    if (r >= 150 and r <= 225) and (g >= 50 and g <= 80) and (b >= 123 and b <= 170):
        return 'H'
    
    # I = YELLOW
    if (r >= 102 and r <= 255) and (g >= 102 and g <= 255) and (b >= 0 and b <= 153):
        return 'I'
    
    # J = PURPLE
    if (r >= 50 and r <= 178) and (g >= 0 and g <= 130) and (b >= 100 and b <= 255):
        return 'J'
    
    # K = LIGHT GREEN
    if (r >= 128 and r <= 175) and (g >= 170 and g <= 240) and (b >= 125 and b <= 205):
        return 'K'
    
    # L = GRAY
    if (r >= 110 and r <= 155) and (g >= 130 and g <= 230) and (b >= 160 and b <= 250):
        return 'L'
    
    # If no piece matches, consider it an empty space
    return '-'

def build_command():
    image = "EEGGGJJJJ--,AEEEGCDDDD-,AAALGCHHD--,BBLLLCFHH--,BBBLCCFFH--"
    args = f"-m normal -i {image}"
    return f"./gradlew run --args=\'{args}\'"

def solve_config():
    cwd = f"{os.getcwd()}/kanoodle-algorithm"
    result = subprocess.run(build_command(), shell=True, capture_output=True, text=True, cwd=cwd)
    solved_config = result.stdout.split(NORMAL_MODE_PREFIX)[1].strip()
    print(solved_config)

def draw_board(img):
    for i in range(1, ROWS + 1):
        for j in range(1, COLS + 1):
            cv2.circle(img, (j * CIRCLE_INCREMENT + OFFSET_LEFT, i * CIRCLE_INCREMENT + OFFSET_TOP), 20, (255, 255, 255), 2)

def crop_circle(img, center):
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8) # Empty black mask
    cv2.circle(mask, center, 20, 255, -1)  # Fill in white circle
    cropped_img = cv2.bitwise_and(img, mask)
    return np.copy(cropped_img)

def crop_circles(img):
    h, w = img.shape[:2]

    mask = np.zeros((h, w), np.uint8)
    cv2.circle(mask, center, 20, 255, -1)

    result = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(mask)
    cropped_result = result[y:y+h, x:x+w]

    return cropped_result

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

    print("Processing image...")

    cv2.imshow("test", crop_circle_2(img, (1 * CIRCLE_INCREMENT + OFFSET_LEFT, 1 * CIRCLE_INCREMENT + OFFSET_TOP)))
    cv2.waitKey(0)
    cv2.imshow("test", crop_circle_2(img, (2 * CIRCLE_INCREMENT + OFFSET_LEFT, 1 * CIRCLE_INCREMENT + OFFSET_TOP)))
    cv2.waitKey(0)
    cv2.imshow("test", crop_circle_2(img, (3 * CIRCLE_INCREMENT + OFFSET_LEFT, 1 * CIRCLE_INCREMENT + OFFSET_TOP)))
    cv2.waitKey(0)
    cv2.imshow("test", crop_circle_2(img, (4 * CIRCLE_INCREMENT + OFFSET_LEFT, 1 * CIRCLE_INCREMENT + OFFSET_TOP)))
    cv2.waitKey(0)