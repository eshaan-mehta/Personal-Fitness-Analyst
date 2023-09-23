import cv2 as cv
from ultralytics import YOLO
import numpy as np
import torch

WINDOW_NAME = "Physiotherapy Recovery Analyst"

capture = cv.VideoCapture(0)




if torch.backends.cudnn.is_available():
    device = "cudnn"
if torch.backends.mps.is_available():
    device = "mps" 
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
print(device)

model = YOLO("yolov8s-pose.pt").to(device) #pretrained model

#keypoints numbers
#0 = nose
#1 = left-eye
#2 = right-eye
#3 = left-ear
#4 = right-ear
#5 = left-shoulder
#6 = right-shoulder
#7 = left-elbow
#8 = right-elbow
#9 = left-wrist
#10 = right-wrist
#11 = left-hip
#12 = right-hip
#13 = left-knee
#14 = right-knee
#15 = left-ankle
#16 = right-ankle