import numpy as np

import subprocess
import os
import cv2

NORMAL_MODE_PREFIX = "[NORMAL_MODE]"
DELIMITER = ","
ROWS = 5
COLS = 11
CIRCLE_RADIUS = 20
CIRCLE_THICKNESS = 2
CIRCLE_COLOR = (255, 255, 255)
CIRCLE_INCREMENT = 50
OFFSET_LEFT = 25  # Move the board shape a bit to the right
OFFSET_TOP = 100  # Move the board shape a bit down

def get_piece_letter(r, g, b):
    print(r, g, b)
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
    mask = np.zeros((h, w), np.uint8)
    cv2.circle(mask, calculate_center(i, j), CIRCLE_RADIUS, CIRCLE_COLOR, -1)
    result = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(mask)
    return result[y : y + h, x : x + w]

def build_config(img):
    config = ""
    for i in range(1, 1 + 1):
            for j in range(1, 1 + 1):
                cropped_img = crop_circle(img.copy(), i, j)
                cv2.imshow("test", cropped_img)
                cv2.waitKey(0)
                config += determine_letter(cropped_img)
            
            if i != ROWS:
                config += DELIMITER

    return config

def determine_letter(cropped_img):
    r, g, b = cv2.split(cropped_img)
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
    return get_piece_letter(int(r_avg),int(g_avg),int(b_avg))

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
    config = build_config(img)
    print(config)