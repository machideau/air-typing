import sys
print("Testing imports...")
try:
    print("Importing cv2...")
    import cv2
    print("cv2 imported.")
except Exception as e:
    print(f"cv2 failed: {e}")

try:
    print("Importing mediapipe base...")
    import mediapipe as mp
    print("mediapipe base imported.")
except Exception as e:
    print(f"mediapipe base failed: {e}")

try:
    print("Importing mediapipe.tasks...")
    from mediapipe.tasks import python
    print("mediapipe.tasks imported.")
except Exception as e:
    print(f"mediapipe.tasks failed: {e}")

try:
    print("Importing mediapipe.tasks.python.vision...")
    from mediapipe.tasks.python import vision
    print("mediapipe.tasks.python.vision imported.")
except Exception as e:
    print(f"mediapipe.tasks.python.vision failed: {e}")
