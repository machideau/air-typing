import traceback
import sys

print("STEP 1: Import cv2")
import cv2
print("STEP 2: Import mediapipe")
import mediapipe as mp
print("STEP 3: Import pygame")
import pygame
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print("STEP 4: Setup Options")
try:
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5)
    print("Options created successfully.")
    
    print("STEP 5: Create Landmarker")
    landmarker = HandLandmarker.create_from_options(options)
    print("Landmarker created successfully.")

except Exception:
    traceback.print_exc()
