
print("Start script")
import os
import sys
print(f"Python Executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print(f"Path: {os.environ.get('PATH')}")

try:
    print("Importing mediapipe...")
    import mediapipe
    print("Mediapipe imported successfully")
except ImportError as e:
    print(f"Failed to import mediapipe: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
