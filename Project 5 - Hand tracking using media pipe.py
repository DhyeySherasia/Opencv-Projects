import cv2
import mediapipe as mp
import pyautogui
import math
# import speech_recognition as sr
# import time
# import numpy as np

cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
pyautogui.FAILSAFE = False
clicked = False
previous_time = 0
current_time = 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False, 1, 0.7, 0.5)
mp_draw = mp.solutions.drawing_utils

pt_0 = []
pt_5 = []
pt_9 = []
pt_13 = []
pt_17 = []
pt_8 = []
pt_12 = []
pt_16 = []
pt_20 = []
pt_3 = []
pt_4 = []
pt_2 = []
pt_7 = []
pt_6 = []
pt_1 = []
centre_points = []
mean_of_points = []


def distance(x1, y1, x2, y2):
    return math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))


def detecting_hand(my_hands):
    if my_hands.multi_hand_landmarks:
        for hand_landmarks in my_hands.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                # print(id, cx, cy, cz)
                if id == 0:
                    pt_0.append([cx, cy])
                elif id == 5:
                    pt_5.append([cx, cy])
                elif id == 9:
                    pt_9.append([cx, cy])
                elif id == 13:
                    pt_13.append([cx, cy])
                elif id == 17:
                    pt_17.append([cx, cy])
                elif id == 8:
                    pt_8.append([cx, cy])
                elif id == 12:
                    pt_12.append([cx, cy])
                elif id == 16:
                    pt_16.append([cx, cy])
                elif id == 20:
                    pt_20.append([cx, cy])
                elif id == 3:
                    pt_3.append([cx, cy])
                elif id == 4:
                    pt_4.append([cx, cy])
                elif id == 2:
                    pt_2.append([cx, cy])
                elif id == 1:
                    pt_1.append([cx, cy])
                elif id == 7:
                    pt_7.append([cx, cy])
                elif id == 6:
                    pt_6.append([cx, cy])

            cal_final_point()

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)


def cal_final_point():
    global clicked
    paused = False

    x1 = (pt_5[-1][0] + pt_9[-1][0] + pt_13[-1][0] + pt_17[-1][0]) / 4
    y1 = (pt_5[-1][1] + pt_9[-1][1] + pt_13[-1][1] + pt_17[-1][1]) / 4

    xc = int((x1 + pt_0[-1][0]) / 2)
    yc = int((y1 + pt_0[-1][1]) / 2)
    cv2.circle(img, (xc, yc), 5, (255, 255, 0), -1)

    centre_points.append([xc, yc])

    # xc = int(xc + ((xc - 320) * 3))
    # yc = int(yc + ((yc - 240) * 3))

    if len(centre_points) >= 7:

        if distance(centre_points[-1][0], centre_points[-1][1], centre_points[-2][0], centre_points[-2][1]) >= 5:
            xc = (centre_points[-2][0] + 0.7 * (centre_points[-2][0] - centre_points[-1][0]))
            yc = centre_points[-2][1] + 0.7 * (centre_points[-2][1] - centre_points[-1][1])

        else:
            xc = (centre_points[-2][0] + 0.1 * (centre_points[-2][0] - centre_points[-1][0]))
            yc = centre_points[-2][1] + 0.1 * (centre_points[-2][1] - centre_points[-1][1])

        max_x = centre_points[-1][0]
        min_x = centre_points[-2][0]
        max_y = centre_points[-1][1]
        min_y = centre_points[-2][1]

        if not paused:
            for i in range(-1, -6, -1):
                if centre_points[i][0] >= max_x:
                    max_x = centre_points[i][0]
                if centre_points[i][1] >= max_y:
                    max_y = centre_points[i][1]
                if centre_points[i][0] <= min_x:
                    min_x = centre_points[i][0]
                if centre_points[i][1] <= min_y:
                    min_y = centre_points[i][1]

            if distance(max_x, max_y, min_x, min_y) <= 5:
                paused = True
            else:
                paused = False

    if not paused:
        x_cursor = (5 * xc) - 700
        y_cursor = (5 * yc) - 700
        pyautogui.moveTo(x_cursor, y_cursor)

    if len(centre_points) >= 2:
        if distance(pt_5[-1][0], pt_5[-1][1], pt_4[-1][0], pt_4[-1][1]) < distance(pt_2[-1][0], pt_2[-1][1],
                                                                                   pt_1[-1][0], pt_1[-1][1]):
            x_cursor, y_cursor = pyautogui.position()
            pyautogui.leftClick(x_cursor, y_cursor)

        elif distance(pt_8[-1][0], pt_8[-1][1], pt_12[-1][0], pt_12[-1][1]) < distance(pt_7[-1][0], pt_7[-1][1],
                                                                                       pt_6[-1][0], pt_6[-1][1]):
            x_cursor, y_cursor = pyautogui.position()
            pyautogui.doubleClick(x_cursor, y_cursor, interval=0.2)

            # r = sr.Recognizer()
            # with sr.Microphone() as source:
            #     r.adjust_for_ambient_noise(source)
            #     input_audio = r.listen(source)
            #
            #     try:
            #         query = r.recognize_google(input_audio, language='en-in')
            #         pyautogui.typewrite(query, interval=0.25)
            #         pyautogui.press('return')
            #     except Exception as e:
            #         print(e)


while cap.isOpened():
    ret, img = cap.read()
    h, w, c = img.shape
    img = cv2.flip(img, 1)
    RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    my_hands = hands.process(RGB_img)
    detecting_hand(my_hands)
    # print(my_hands.multi_hand_landmarks)

    cv2.imshow("Hand", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
