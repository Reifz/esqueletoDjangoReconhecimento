from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import json
import base64
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'SEU_EMAIL@gmail.com' and password == 'admin':
            return redirect('core:recognize')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def recognize_view(request):
    if request.method == 'POST':
        temp_img_path = None
        try:
            data = json.loads(request.body)
            image_data = data['image']
            
            # Decode the base64 image
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            img_data = base64.b64decode(imgstr)
            
            # Convert to an image that cv2 can use
            nparr = np.frombuffer(img_data, np.uint8)
            img_captured = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Create a temporary file
            fd, temp_img_path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)

            # Save the image to the temporary path
            cv2.imwrite(temp_img_path, img_captured)

            # Path to the reference image
            reference_image_path = settings.BASE_DIR / 'foto4.jpg'

            # Verify the face
            print("Performing face verification...")
            result = DeepFace.verify(
                img1_path=str(reference_image_path),
                img2_path=temp_img_path, # Pass the path
                model_name='VGG-Face',
                enforce_detection=False
            )
            print("Verification complete.")

            return JsonResponse({'verified': result['verified'], 'distance': result['distance']})
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            # Clean up the temporary file
            if temp_img_path and os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
    return render(request, 'core/recognize.html')

def home_view(request):
    return render(request, 'core/home.html')
