from setup import *

MIN_CONFIDENCE = 0.5
OVERLAY_HEIGHT = 100

left_knee_angle = 0
right_knee_angle = 0
knee_to_ankle_x = 0
back_straightness = 1 #percentage
depth = 0 #percentage

def overlay(frame: cv.Mat, left_angle: float, right_angle: float) -> cv.Mat:
    #frame shape = (height, width, depth)
    
    #background rectangle
    frame = cv.rectangle(img=frame,
                         pt1=(0, frame.shape[0] - OVERLAY_HEIGHT),
                         pt2=(frame.shape[1], frame.shape[0]),
                         color=(0,0,0),
                         thickness=cv.FILLED
                         )
    #left knee angle text
    frame = cv.putText(img=frame,
                       text="Left Knee Angle: " + str(round(left_angle, 1)),
                       org=(5, frame.shape[0] - OVERLAY_HEIGHT + 25),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)
    
    #right knee angle text
    frame = cv.putText(img=frame,
                       text="Right Knee Angle: " + str(round(right_angle, 1)),
                       org=(5, frame.shape[0] - OVERLAY_HEIGHT + 65),
                       fontFace=cv.FONT_HERSHEY_SIMPLEX,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)

    return frame


def find_angle(start: list, middle: list, end: list) -> float:
    #calculate angle and convert to degrees
    angle = np.arctan2(start[1] - middle[1], start[0] - middle[0]) - np.arctan2(end[1] - middle[1], end[0] - middle[0])
    angle = np.abs(angle * 180/np.pi)
    
    #ensures angle between 0-180 degrees
    return (360 - angle) if angle > 180 else angle


while capture.isOpened():
    success, frame = capture.read() #extracts single frame from video, success if receiving video

    if success:
        results = model(source=frame, verbose=False, conf=MIN_CONFIDENCE)

        for person in results:
            #index 0 to go down one dimension within tensor
            #only care about hip, knees, ankle keypoints
            keypoints = person.keypoints.xy[0][11:].tolist() 

            if len(keypoints > 0):    
                #calculating angles at knees
                left_knee_angle = find_angle(keypoints[0], keypoints[2], keypoints[4])
                right_knee_angle = find_angle(keypoints[1], keypoints[3], keypoints[5])
                
            annotated_frame = person.plot()#adding person bounding box to frame

        #annotated_frame = cv.flip(annotated_frame, 1) #flip image horizontally
        annotated_frame = overlay(annotated_frame, left_knee_angle, right_knee_angle)
        cv.imshow(WINDOW_NAME, annotated_frame) #display framerate and flip camera horzontally

        #program waits 1ms each between frames checks for keypress of escape
        # 27 is ASCII of escape key
        if (cv.waitKey(1) & 0xFF) == ord('q'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows()