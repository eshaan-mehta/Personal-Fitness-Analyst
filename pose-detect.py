from setup import *

pose_model = YOLO("yolov8s-pose.pt")

results = pose_model('https://ultralytics.com/images/bus.jpg') 