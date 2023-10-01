from setup import *

OVERLAY_HEIGHT = 100
FRAME_INTERVAL = 5

MIN_CONFIDENCE = 0.5
UP_THRESHOLD = 150
DOWN_THRESHOLD = 100
BALANCE_THRESHOLD = 20

STATUS_LIST = {0:"OFF", 1:"RESET", 2:"ACTIVE"}
STATUS_COLOR = {0:(0,0,0), 1:(0,0,160), 2:(0,190,0)}
status = 0

front_knee = []
back_knee = []
back_side = []
front_leg = ""

#points for analytics
frames = []
depth_points = []
back_points = []
balance_points = []
frame_count = 0

def reset() -> None:
    global front_knee_angle, back_knee_angle, hip_angle
    global back_straightness, knee_to_ankle_x, depth, balance, cur_shoulders, prev_shoulders, num_reps, is_up

    front_knee_angle = 0
    back_knee_angle = 0
    hip_angle = 0

    back_straightness = 0 #percentage
    balance = 0
    cur_shoulders = 0 
    prev_shoulders = 0


    num_reps = 0
    is_up = True


def find_angle(start: list, middle: list, end: list) -> float:
    #calculate angle and convert to degrees
    angle = arctan2(start[1] - middle[1], start[0] - middle[0]) - arctan2(end[1] - middle[1], end[0] - middle[0])
    angle = abs(angle * 180/pi)

    #ensures angle between 0-180 degrees
    return (360 - angle) if angle > 180 else angle

def deviation(target: float, range: float, angle: float) -> float:
    #converts angle to percentage based of deviation from specified target
    # maps angle to [0,1] * 100

    percent = 1 - abs(target - angle)/range

    return 0 if (target - angle > range) else round(percent*100, 2)

def overlay(frame: cv.Mat) -> cv.Mat:
    #frame shape = (height, width, depth)
    #color is in BGR
    
    #status background
    frame = cv.rectangle(img=frame,
                         pt1=(frame.shape[1]//4*3, 0),
                         pt2=(frame.shape[1], frame.shape[0]//10),
                         color=STATUS_COLOR[status],
                         thickness=cv.FILLED
                         )
    
    frame = cv.putText(img=frame,
                       text=STATUS_LIST[status],
                       org=(frame.shape[1]//4*3 + 25, 50),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=2.5,
                       color=(255,255,255),
                       thickness=2)

#-----------------------------------------------------------------------------
    
    #rep background
    frame = cv.rectangle(img=frame,
                         pt1=(0,0),
                         pt2=(frame.shape[1]//3, frame.shape[0]//10),
                         color=(160,0,0),
                         thickness=cv.FILLED
                         )
    
    #rep counter
    frame = cv.putText(img=frame,
                       text=f"Reps: {num_reps}",
                       org=(25, 50),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=2.5,
                       color=(255,255,255),
                       thickness=2)
    
    #up/down status
    frame = cv.putText(img=frame,
                       text= "up" if is_up else "down",
                       org=(300, 50),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale= 1.7,
                       color=(255,255,255),
                       thickness=1)

#-----------------------------------------------------------------------------

    #bottom background rectangle
    frame = cv.rectangle(img=frame,
                         pt1=(0, frame.shape[0] - OVERLAY_HEIGHT),
                         pt2=(frame.shape[1], frame.shape[0]),
                         color=(0,0,0),
                         thickness=cv.FILLED
                         )
    
    #front knee angle text
    frame = cv.putText(img=frame,
                       text=f"Front Knee Angle: {round(front_knee_angle, 2)}",
                       org=(25, frame.shape[0] - OVERLAY_HEIGHT + 25),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=1.2,
                       color=(255,255,255),
                       thickness=2)
    
    #back knee angle text
    frame = cv.putText(img=frame,
                       text=f"Back Knee Angle: {round(back_knee_angle, 2)}",
                       org=(25, frame.shape[0] - OVERLAY_HEIGHT + 65),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=1.2,
                       color=(255,255,255),
                       thickness=2)
    
    #back straightness
    frame = cv.putText(img=frame,
                       text=f"Back Straighness: {back_straightness}%",
                       org=(frame.shape[1]//3*2, frame.shape[0] - OVERLAY_HEIGHT + 25),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=1.2,
                       color=(255,255,255),
                       thickness=2)
    
    #front leg
    frame = cv.putText(img=frame,
                       text=f"Front leg: {front_leg}",
                       org=(frame.shape[1]//3, frame.shape[0] - OVERLAY_HEIGHT//2),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=1.2,
                       color=(255,255,255),
                       thickness=2)

    #balance
    frame = cv.putText(img=frame,
                       text=f"Balance: {balance}",
                       org=(frame.shape[1]//3*2, frame.shape[0] - OVERLAY_HEIGHT + 65),
                       fontFace=cv.FONT_HERSHEY_COMPLEX_SMALL,
                       fontScale=1.2,
                       color=(255,255,255),
                       thickness=2) 
    
    """
    if status == 1:
        frame = cv.circle(img=frame, 
                          center=(int(keypoints[5][0]), int(keypoints[5][1])),
                          radius=15,
                          color=status_color[status],
                          thickness=cv.FILLED)
        frame = cv.circle(img=frame, 
                          center=(int(keypoints[6][0]), int(keypoints[6][1])),
                          radius=15,
                          color=status_color[status],
                          thickness=cv.FILLED)
        frame = cv.circle(img=frame, 
                          center=(int(keypoints[7][0]), int(keypoints[7][1])),
                          radius=15,
                          color=status_color[status],
                          thickness=cv.FILLED)
        frame = cv.circle(img=frame, 
                          center=(int(keypoints[8][0]), int(keypoints[8][1])),
                          radius=15,
                          color=status_color[status],
                          thickness=cv.FILLED)
    """
    return frame


reset()
while capture.isOpened():
    success, frame = capture.read() #extracts single frame from video, success if receiving video

    if not success:
        break
    else:
        results = model(source=frame, verbose=False, conf=MIN_CONFIDENCE)
        

        for person in results:
            #index 0 to go down one dimension within tensor
            #bring keypoints back to cpu and convert to list
            keypoints = person.keypoints.xy[0].cpu().tolist() 

            #use try, except block to prevent crashes if error arises for a frame
            try:  
                #define relevent front, back keypoints list depending on direction of person and knee in front
                if keypoints[1][0] < keypoints[3][0]: #user facing camera left
                    if keypoints[15][0] < keypoints[16][0]: #left leg forward
                        front_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_side = [keypoints[5], keypoints[11], keypoints[14]] #right
                        front_leg = "Left"

                    else: #right leg forward
                        front_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_side = [keypoints[6], keypoints[12], keypoints[13]] #left
                        front_leg = "Right"
                if keypoints[1][0] >= keypoints[3][0]: #user facing camera right
                    if keypoints[15][0] > keypoints[16][0]: #left leg forward
                        front_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_side = [keypoints[5], keypoints[11], keypoints[14]] #right
                        front_leg = "Left"

                    else: #right leg forward
                        front_knee = [keypoints[12], keypoints[14], keypoints[16]] #right
                        back_knee = [keypoints[11], keypoints[13], keypoints[15]] #left
                        back_side = [keypoints[6], keypoints[12], keypoints[13]] #left
                        front_leg = "Right"

                prev_shoulders = abs(keypoints[5][1] - keypoints[6][1])

                #tracking user status if in active status
                if status == 2:
                    #calculating angles at knees, hip
                    front_knee_angle = find_angle(front_knee[0], front_knee[1], front_knee[2])
                    back_knee_angle = find_angle(back_knee[0], back_knee[1], back_knee[2])
                    hip_angle = find_angle(back_side[0], back_side[1], back_side[2])

                    cur_shoulders = abs(keypoints[5][1] - keypoints[6][1])

                    balance = deviation(prev_shoulders, BALANCE_THRESHOLD, cur_shoulders)
                    
                    #calculate back straighness using hip angle
                    back_straightness = deviation(157, 80, hip_angle)

                    #counting repts
                    if front_knee_angle > UP_THRESHOLD and not is_up:
                        num_reps += 1
                        is_up = True
                    elif is_up and (front_knee_angle < DOWN_THRESHOLD):
                        is_up = False

                #set status to reset if elbows above shoulders
                #note: y is increase as you go down the screen
                if keypoints[7][1] < keypoints[5][1] and keypoints[8][1] < keypoints[6][1]:
                    status = 1

                    #reset stats if not already reset
                    if front_knee_angle > 0:
                        reset()
                elif status != 0: #set to active status when not in off status
                    status = 2
                
            except:
                print(Exception)
            
            annotated_frame = person.plot() #adding person bounding box to frame


        annotated_frame = overlay(annotated_frame) #adding all overlay
        
        #cv.resizeWindow(WINDOW_NAME, 900, 700)
        cv.imshow(WINDOW_NAME, annotated_frame) #display frame

        #program waits 1ms each between frames checks for keypress of 'q'
        if (cv.waitKey(1) & 0xFF) == ord('q'):
            break
    

capture.release()
cv.destroyAllWindows()
