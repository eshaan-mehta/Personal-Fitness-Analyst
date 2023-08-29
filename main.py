import cv2 as cv
from ultralytics import YOLO

capture = cv.VideoCapture(0)

while(True):

    _, frame = capture.read()

    cv.imshow("video capture", cv.flip(frame, 1))

    if cv.waitKey(1) & 0xFF == 27:
        break

capture.release()
cv.destroyAllWindows()
