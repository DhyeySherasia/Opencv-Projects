import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
lower_b = np.array([104, 137, 86])
upper_b = np.array([114, 222, 146])
lower_g = np.array([67, 74, 72])
upper_g = np.array([90, 155, 150])
blue_points = []
pyautogui.FAILSAFE = False
first = False


def control_cursor(x, y, green_present, first):
    xc = 3 * x
    yc = 3 * y
    pyautogui.moveTo(x=xc, y=yc)
    if green_present and not first:
        pyautogui.click(x=xc, y=yc, clicks=1, interval=0.0, button='left')


def detect_colour(frame):
    global first
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_b = cv2.inRange(hsv_frame, lower_b, upper_b)
    mask_g = cv2.inRange(hsv_frame, lower_g, upper_g)
    ret, thresh_g = cv2.threshold(mask_g, 127, 255, cv2.THRESH_BINARY)
    ret, thresh_b = cv2.threshold(mask_b, 127, 255, cv2.THRESH_BINARY)
    x_b, y_b = get_contours(thresh_b, 1)
    blue_points.append((x_b, y_b))
    x_g, y_g = get_contours(thresh_g, 0)
    cv2.circle(org_frame, (x_b, y_b), 5, (255, 255, 0), -1)
    cv2.circle(org_frame, (x_g, y_g), 5, (0, 255, 0), -1)
    if x_g != -5:
        control_cursor(x_b, y_b, True, first)
        first = True
    else:
        first = False
        control_cursor(x_b, y_b, False, first)


def get_contours(thresh, colour):
    contours, ret = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y = -5, -5
    if colour == 1:
        x = int(pyautogui.position()[0] / 3)
        y = int(pyautogui.position()[1] / 3)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if area > 20:
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])

            return x, y
    return x, y


while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    org_frame = frame.copy()
    detect_colour(frame)

    cv2.imshow("Org_frame", org_frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
