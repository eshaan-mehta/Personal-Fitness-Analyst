import cv2 as cv
import time
from ultralytics import YOLO
import numpy as np

capture = cv.VideoCapture(0)
WINDOW_NAME = "Video Capture"


pose_model = YOLO("yolov8s-pose.pt") #pretrained model