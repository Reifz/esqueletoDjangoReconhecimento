from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.urls import reverse

from core.forms import UserRegisterForm
from . models import LogAcesso, Usuario
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
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            request.session['user_id'] = user.id
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
            if not user_id:
                return JsonResponse({'error': 'Usuário não logado'}, status=400)

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
            print("Realizando verificação facial...")
            result = DeepFace.verify(
                img1_path=str(reference_image_path),
                img2_path=temp_img_path,
                model_name='VGG-Face',
                enforce_detection=False
            )
            print("Verificação concluída.")

            # Registrar o acesso no log
            if result['verified']:
                # Acesso aprovado
                LogAcesso.objects.create(
                    usuario=user,
                    result=LogAcesso.RESULT_APPROVED
                )
                return JsonResponse({
                    'verified': True, 
                    'redirect_url': reverse('core:home')
                })
            else:
                # Acesso negado
                LogAcesso.objects.create(
                    usuario=user,
                    result=LogAcesso.RESULT_DENIED
                )
                return JsonResponse({
                    'verified': False, 
                    'distance': result['distance']
                })
                
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            # Registrar tentativa falha (quando possível identificar o usuário)
            if 'user' in locals():
                LogAcesso.objects.create(
                    usuario=user,
                    result=LogAcesso.RESULT_DENIED
                )
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            # Clean up the temporary file
            if temp_img_path and os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
    return render(request, 'core/recognize.html')

def home_view(request):
    return render(request, 'core/home.html')
