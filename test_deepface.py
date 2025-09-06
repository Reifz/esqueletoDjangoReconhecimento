import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'
from deepface import DeepFace
import cv2

print("DeepFace imported successfully")

try:
    img = cv2.imread("foto4.jpg")
    if img is None:
        print("Could not read image")
    else:
        print("Image read successfully")
        results = DeepFace.analyze(img, actions=['emotion'])
        print(results)
except Exception as e:
    print(f"An error occurred: {e}")
