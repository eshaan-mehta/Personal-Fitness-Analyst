from setup import *


MIN_CONFIDENCE = 0.5

left_knee_angle = 0
right_knee_angle = 0
knee_to_angkle_x = 0
back_straightness = 1 #percentage
depth = 0 #percentage

required_keypoints = ["left_shoulder", "right_shoulder", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle",]


def overlay(frame):
    #adding FPS overlay onto video
    frame = cv.putText(img=frame,
                    text="FPS: " + str(fps),
                    org=(7, 30),
                    fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, 
                    color=(100, 255, 0),
                    thickness=2,
                    )

    


prev_time = time.time()  #initial time calculation
while(capture.isOpened()):
    #delta_time calculation to determine time per frame
    cur_time = time.time()
    delta_time = cur_time - prev_time if cur_time != prev_time else 1 #to remove divide by 0 case
    prev_time = cur_time
    fps = int(1/delta_time)

    success, frame = capture.read() #extracts single fram from video, success shows if receiving video

    if success:

        results = model(source=frame, verbose=False, conf=MIN_CONFIDENCE)

        for person in results:

            keypoint_list = []

            keypoints = person.keypoints.data[0]

            print(keypoints)
            keypoint_list.append(keypoints)

            annotated_frame = person.plot()

        for keypoint in required_keypoints:
            if(keypoint not in keypoint_list):
                print("Please move into camera view")




        #annotated_frame = cv.flip(annotated_frame, 1) #flip image horizontally
        #overlay(annotated_frame) #adding overlay to video
        annotated_frame = cv.putText(img=annotated_frame,
                    text="FPS: " + str(fps),
                    org=(7, 30),
                    fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, 
                    color=(100, 255, 0),
                    thickness=2,
                    )
        cv.imshow(WINDOW_NAME, annotated_frame) #display framerate and flip camera horzontally

        #program waits 1ms each between frames checks for keypress of escape
        # 27 is ASCII of escape key
        if (cv.waitKey(1) & 0xFF) == 27:
            break
    else:
        break

    
capture.release()
cv.destroyAllWindows()
