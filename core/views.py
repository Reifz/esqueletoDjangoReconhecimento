from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.conf import settings

from core.forms import UserRegisterForm
from . models import Usuario
import json
import base64
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os

def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Usuario.objects.get(email=email)
            if user.verify_password(password):
                request.session["user_id"] = user.id
                return redirect("core:recognize")
            else:
                error = "Senha incorreta"
        except Usuario.DoesNotExist:
            error = "Usuário não encontrado"
    return render(request, "core/login.html", {"error": error})


def register_view(request):
    if request.method == 'POST':
<<<<<<< HEAD
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            request.session['user_id'] = user.id
=======
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'SEU_EMAIL@gmail.com' and password == 'admin':
>>>>>>> 4fdd18e548013740a0d5d4dd16aa5b78f8cd7e2e
            return redirect('core:recognize')
        else:
            # Retorna o formulário com erros
            return render(request, 'core/register.html', {'form': form})

    else:
        form = UserRegisterForm()
        return render(request, 'core/register.html', {'form': form})


def recognize_view(request):
    if request.method == 'POST':
        temp_img_path = None
        try:

            user_id = request.session.get('user_id')

            user = Usuario.objects.get(id=user_id)

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
            reference_image_path = user.photo.path

            # Verify the face
            print("Performing face verification...")
            result = DeepFace.verify(
                img1_path=str(reference_image_path),
                img2_path=temp_img_path, # Pass the path
                model_name='VGG-Face',
                enforce_detection=False
            )
            print("Verification complete.")

            if result['verified'] == True:

                return render(request, "core/home.html", {'user': user})

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
