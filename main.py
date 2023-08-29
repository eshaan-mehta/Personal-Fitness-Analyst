from setup import *


prev_time = time.time()  #initial time calculation

while(True):
    #delta_time calculation to determine time per frame
    cur_time = time.time()
    delta_time = cur_time - prev_time if cur_time != prev_time else 1 #to remove divide by 0 case
    prev_time = cur_time
    fps = int(1/delta_time)

    ret, frame = capture.read() #extracts single fram from video, ret is failure to receive video

    #flip image horizontally and overlay frame rate 
    frame = cv.flip(frame, 1)
    frame = cv.putText(img=frame,
                       text="FPS: " + str(fps),
                       org=(7, 30),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=1, 
                       color=(100, 255, 0),
                       thickness=2,
                       )

    cv.imshow(WINDOW_NAME, frame) #display framerate and flip camera horzontally

    #program waits 1ms each between frames checks for keypress of escape
    # 27 is ASCII of escape key
    if (cv.waitKey(1) & 0xFF) == 27 or not ret:
        break

    
capture.release()
cv.destroyAllWindows()
