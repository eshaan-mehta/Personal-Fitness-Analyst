from setup import *

MIN_CONFIDENCE = 0.5
overlay_height = 100
UP_THRESHOLD = 150
DOWN_THRESHOLD = 100

front_knee = []
back_knee = []
back_side = []

front_knee_angle = 0
back_knee_angle = 0
hip_angle = 0
front_leg = ""



knee_to_ankle_x = 0
back_straightness = 1 #percentage
depth = 0 #percentage
balance = 0 #percentage

num_reps = 0
is_up = True

def overlay(frame: cv.Mat) -> cv.Mat:
    #frame shape = (height, width, depth)
    

    #background rectangle
    frame = cv.rectangle(img=frame,
                         pt1=(0, frame.shape[0] - overlay_height),
                         pt2=(frame.shape[1], frame.shape[0]),
                         color=(0,0,0),
                         thickness=cv.FILLED
                         )
    #left knee angle text
    frame = cv.putText(img=frame,
                       text=f"Front Angle: {round(front_knee_angle, 2)}",
                       org=(5, frame.shape[0] - overlay_height + 15),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)
    
    #right knee angle text
    frame = cv.putText(img=frame,
                       text=f"Back Angle: {round(back_knee_angle, 2)}",
                       org=(5, frame.shape[0] - overlay_height + 45),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)
    
    #rep counter
    frame = cv.putText(img=frame,
                       text=f"Reps: {hip_angle}",
                       org=(frame.shape[1] - 300, frame.shape[0] - overlay_height + 15),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)
    
    #front leg
    is_up_text = "up" if is_up else "down"
    frame = cv.putText(img=frame,
                       text= "up" if is_up else "down",
                       org=(frame.shape[1] - 300, frame.shape[0] - overlay_height + 45),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=0.8,
                       color=(255,255,255),
                       thickness=2)
    #back straightness
    frame = cv.putText(img=frame,
                       text=f"Back Straighness: {back_straightness}%",
                       org=(frame.shape[1] - 300, frame.shape[0] - overlay_height + 75),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
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

def to_percent(goal: float, range: float, angle: float) -> float:
    #converts angle to percentage for desired angle range
    # maps angle to [0,1] * 100

    percent = 1 - abs(goal - angle)/range

    return 0 if (goal - angle > range) else round(percent*100, 2)


while capture.isOpened():
    success, frame = capture.read() #extracts single frame from video, success if receiving video

    if success:
        results = model(source=frame, verbose=False, conf=MIN_CONFIDENCE)

        for person in results:
            #index 0 to go down one dimension within tensor
            #only care about hip, knees, ankle keypoints
            keypoints = person.keypoints.xy[0].tolist() 

            try:  
                if keypoints[1][0] < keypoints[3][0]: #facing camera left
                    if keypoints[15][0] < keypoints[16][0]: #left leg forward
                        front_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_side = [keypoints[5], keypoints[11], keypoints[14]] #right
                        front_leg = "Left Leg front"

                    else: #right leg forward
                        front_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_side = [keypoints[6], keypoints[12], keypoints[13]] #left
                        front_leg = "Right Leg front"

                if keypoints[1][0] >= keypoints[3][0]: #facing camera right
                    if keypoints[15][0] > keypoints[16][0]: #left leg forward
                        front_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_side = [keypoints[5], keypoints[11], keypoints[14]] #right
                        front_leg = "Left Leg front"

                    else: #right leg forward
                        front_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_side = [keypoints[6], keypoints[12], keypoints[13]] #left
                        front_leg = "Right Leg front"

                #calculating angles at knees, hip
                front_knee_angle = find_angle(front_knee[0], front_knee[1], front_knee[2])
                back_knee_angle = find_angle(back_knee[0], back_knee[1], back_knee[2])
                hip_angle = find_angle(back_side[0], back_side[1], back_side[2])

                if is_up:
                    back_straightness = to_percent(165, 70, hip_angle)
                else:
                    back_straightness = to_percent(170, 80, hip_angle)

                if front_knee_angle > UP_THRESHOLD and not is_up:
                    num_reps += 1
                    is_up = True
                elif is_up and (front_knee_angle < DOWN_THRESHOLD):
                    is_up = False
            except:
                pass
            
            annotated_frame = person.plot()#adding person bounding box to frame

        #annotated_frame = cv.flip(annotated_frame, 1) #flip image horizontally
        annotated_frame = overlay(annotated_frame)
        
        #cv.resizeWindow(WINDOW_NAME, 900, 700)
        cv.imshow(WINDOW_NAME, annotated_frame) #display framerate and flip camera horzontally

        #program waits 1ms each between frames checks for keypress of escape
        # 27 is ASCII of escape key
        if (cv.waitKey(1) & 0xFF) == ord('q'):
            break
    else:
        break

capture.release()
cv.destroyAllWindows()
