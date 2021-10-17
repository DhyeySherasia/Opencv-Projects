import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
study_room = True
on_sofa = False

# Study room
if study_room:
    lower_b = np.array([104, 79, 53])
    upper_b = np.array([118, 255, 255])
    lower_g = np.array([70, 32, 53])
    upper_g = np.array([90, 174, 162])

# Sofa place
elif not study_room and on_sofa:
    # on sofa
    lower_b = np.array([104, 113, 60])
    upper_b = np.array([125, 200, 123])
    lower_g = np.array([63, 35, 26])
    upper_g = np.array([98, 132, 87])

elif not study_room and not on_sofa:
    # on tipoi
    lower_b = np.array([98, 28, 90])
    upper_b = np.array([135, 183, 227])
    lower_g = np.array([49, 19, 77])
    upper_g = np.array([100, 88, 156])

blue_pts = []
green_pts = []
first = False


def detect_colour(frame):
    global first
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_b = cv2.inRange(hsv_frame, lower_b, upper_b)
    mask_g = cv2.inRange(hsv_frame, lower_g, upper_g)
    final_mask = cv2.bitwise_or(mask_b, mask_g)
    ret1, thresh_b = cv2.threshold(mask_b, 127, 255, cv2.THRESH_BINARY)
    ret1, thresh_g = cv2.threshold(mask_g, 127, 255, cv2.THRESH_BINARY)
    length_b = get_contours(thresh_b)
    length_g = get_contours(thresh_g)
    if length_b >= 1 and length_g >= 1 and not first:
        pyautogui.hotkey('win', 'prtsc')
        first = True
    elif length_g == 0 or length_b == 0:
        first = False

    return final_mask


def get_contours(thresh):
    contours, ret2 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= 300:
            length = len(contours)
            return length
    return 0


while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh_frame = detect_colour(frame)

    cv2.imshow("Thresh", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
