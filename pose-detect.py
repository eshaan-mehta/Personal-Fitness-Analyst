from setup import *

pose_model = YOLO("yolov8s-pose.pt")

keypoint_names = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

cap = cv.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()

    if success:
        # Pose detection
        pose_results = pose_model(frame, verbose=True, conf=0.5)

        # Print each body coordinate as a dictionary
        for person in pose_results:
            keypoints = person.keypoints.data[0]
            for keypoint, name in zip(keypoints, keypoint_names):
                x, y, probability = keypoint #keypoint is 3d array
                print(
                    {
                        "keypoint": name,
                        "x": x.item(),
                        "y": y.item(),
                        "probability": probability.item(),
                    }
                )

            pose_annotated_frame = person.plot()
            cv.imshow("Pose Detection", pose_annotated_frame)

        if cv.waitKey(1) & 0xFF == 27:
            break
    else:
        break

cap.release()
cv.destroyAllWindows()