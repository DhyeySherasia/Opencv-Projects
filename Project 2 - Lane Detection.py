import cv2
import numpy as np
from matplotlib import pyplot as plt


def roi(img, vertices):
    mask = np.zeros_like(img)
    # Fill polygon with white
    cv2.fillPoly(mask, vertices, 255)
    # Bitwise_and : black + any_colour --> black    white + any_colour --> any_colour
    final_img = cv2.bitwise_and(img, mask)
    return final_img


def draw_lines(img, lines):
    blank_img = np.zeros_like(img)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(blank_img, (x1, y1), (x2, y2), (0, 255, 0), 3)

    final_img = cv2.add(img, blank_img)
    return final_img


# img = cv2.imread("Resources/road_lines.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def process(img):
    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    cv2.imshow("Edges", edges)
    roi_vertices = [(0, height), (width/2, 310), (width, height)]
    cropped_img = roi(edges, np.array([roi_vertices], np.int32))

    lines = cv2.HoughLinesP(cropped_img, rho=4, theta=np.pi/180, threshold=250, minLineLength=40, maxLineGap=200)
    final_lines = draw_lines(img, lines)
    return final_lines


cap = cv2.VideoCapture("Resources/road_lines_2.mp4")

while cap.isOpened():
    ret, img = cap.read()
    final_video_frame = process(img)
    cv2.imshow("Lane Detection", final_video_frame)

    if cv2.waitKey(70) == 27:
        break


cap.release()
cv2.destroyAllWindows()




