import cv2 as cv
import time
from ultralytics import YOLO

capture = cv.VideoCapture(0)


prev_time = time.time()  #initial time calculation

while(True):
    #delta_time calculation to determine time per frame
    cur_time = time.time()
    delta_time = cur_time - prev_time if cur_time != prev_time else 1 #to remove divibe by 0 case
    prev_time = cur_time

    _, frame = capture.read() #extracts single fram from video

    cv.imshow("FPS: " + str(int(1/delta_time)), cv.flip(frame, 1)) #display framerate and flip camera horzontally

    #program waits 1ms each between frames checks for keypress  
    # 27 is ASCII of escape key
    if cv.waitKey(1) & 0xFF == 27:
        break

    
capture.release()
cv.destroyAllWindows()
