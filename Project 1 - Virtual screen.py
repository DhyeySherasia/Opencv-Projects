import cv2
import numpy as np
import math
import urllib.request as ur


cap = cv2.VideoCapture(0)

# my_url = 'http://192.168.50.187:8080/shot.jpg'

# Order - Orange, Green, Blue
my_colours = [[0, 146, 102, 18, 234, 188],
              [67, 74, 72, 90, 155, 150],
              [104, 137, 86, 114, 222, 146]]

# BGR
my_drawing_colours = [[3, 152, 252], [0, 255, 77], [255, 64, 0]]

# [x, y, which colour to draw]
my_points = []


def find_colour(img, my_colours, my_drawing_colours, ):
    global paint_mode, doodle_mode
    count = 0
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for colour in my_colours:
        lower = np.array(colour[0:3])
        upper = np.array(colour[3:6])
        mask = cv2.inRange(hsv_img, lower, upper)
        # cv2.imshow(str(colour[0]), mask)
        ret1, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, np.ones((2, 2), np.uint8), iterations=2)
        x, y = get_contours(dilated)
        if x != 0 and y != 0:
            cv2.circle(img_result, (x, y), 20, my_drawing_colours[count], 2)
            my_points.append([x, y, count])
            if 480 <= x <= 630 and 10 <= y <= 60 and len(my_points) >= 2:
                if not (480 < my_points[len(my_points) - 2][0] < 630 and 10 < my_points[len(my_points) - 2][1] < 60):
                    if paint_mode:
                        paint_mode = False
                        doodle_mode = True
                    elif doodle_mode:
                        doodle_mode = False
                        paint_mode = True
        count += 1


def get_contours(dilated):
    contours, ret2 = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 20:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)

    return x + (w//2), y


def draw_continuous(my_points, my_drawing_colours):
    for i in range(len(my_points)-1):
        # my_points[i][0] --> x  my_points[i][1] --> y  my_points[i][2] --> count
        # cv2.circle(img_result, (point[0], point[1]), 10, my_drawing_colours[point[2]], -1)
        # cv2.circle(white_board, (point[0], point[1]), 10, my_drawing_colours[point[2]], -1)

        count = 0
        j = 0
        while count < 5 and j <= (len(my_points)-5):
            j = i+count+1
            if my_points[i][2] == my_points[j][2] and math.sqrt(pow(my_points[i][0]-my_points[j][0], 2) + pow(my_points[i][1]-my_points[j][1], 2)) <= 100:
                if doodle_mode:
                    cv2.line(img_result, (my_points[i][0], my_points[i][1]), (my_points[j][0], my_points[j][1]), my_drawing_colours[my_points[i][2]], 3)
                elif paint_mode:
                    cv2.line(white_board, (my_points[i][0], my_points[i][1]), (my_points[j][0], my_points[j][1]), my_drawing_colours[my_points[i][2]], 3)
                break
            count += 1


start = True
paint_mode = False
doodle_mode = True
while True:
    # Smartphone camera feed
    # img_response = ur.urlopen(my_url)
    # img_np = np.array(bytearray(img_response.read()), dtype=np.uint8)
    # img = cv2.imdecode(img_np, -1)

    ret, img = cap.read()
    img = cv2.flip(img, 1)
    img_result = img.copy()
    white_board = np.zeros_like(img) + 255
    # white_board = np.zeros((480, 640, 3), np.uint8) + 255

    if cv2.waitKey(1) == ord('s'):
        if start:
            start = False
        else:
            start = True
    elif cv2.waitKey(1) == 32:
        my_points = []
    elif cv2.waitKey(1) == 27:
        break

    if start:
        find_colour(img, my_colours, my_drawing_colours)
        cv2.putText(img_result, "Doodle Mode ON", (15, 20), cv2.FONT_ITALIC, 0.7, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(white_board, "Paint Mode ON", (15, 20), cv2.FONT_ITALIC, 0.7, (255, 255, 0), 2, cv2.LINE_AA)

    if len(my_points) >= 6:
        draw_continuous(my_points, my_drawing_colours)

    switch_mode_button_d = cv2.rectangle(img_result, (480, 10), (630, 60), (234, 235, 230), -1)
    switch_mode_button_p = cv2.rectangle(white_board, (480, 10), (630, 60), (94, 94, 94), -1)
    cv2.putText(img_result, "Switch Mode", (490, 40), cv2.FONT_ITALIC, 0.65, (46, 46, 46), 2, cv2.LINE_AA)
    cv2.putText(white_board, "Switch Mode", (490, 40), cv2.FONT_ITALIC, 0.65, (234, 235, 230), 2, cv2.LINE_AA)

    if doodle_mode:
        cv2.imshow("Result", img_result)
        cv2.destroyWindow("Paint")
    elif paint_mode:
        cv2.imshow("Paint", white_board)
        cv2.destroyWindow("Result")


cap.release()
cv2.destroyAllWindows()
