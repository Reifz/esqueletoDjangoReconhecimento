import json
import base64
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse
from core.forms import UserRegisterForm
from . models import LogAcesso, Usuario

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user) #cria a sessão do usuário
            return redirect('core:recognize')
        else:
            # Retorna o formulário com erros
            return render(request, 'core/register.html', {'form': form})

    else:
        form = UserRegisterForm()
        return render(request, 'core/register.html', {'form': form})

def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:recognize")
        else:
            error = "Credenciais inválidas"

    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    request.user.is_active = False
    logout(request)
    return redirect('core:login')

def recognize_view(request):
    if request.method == 'POST':
        temp_img_path = None
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Usuário não logado'}, status=400)

            user = request.user

            data = json.loads(request.body)
            image_data = data['image']
            
            # Decode the base64 image
            format, imgstr = image_data.split(';base64,') 
            ext = format.split('/')[-1] 
            img_data = base64.b64decode(imgstr)
            
            # Imagem para CV2
            nparr = np.frombuffer(img_data, np.uint8)
            img_captured = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Cria um arquivo temporário
            fd, temp_img_path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)

            # Salva a imagem temporária
            cv2.imwrite(temp_img_path, img_captured)
            
            # Caminho para a referência da imagem para o usuário
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

    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, 'core/home.html', {'user': request.user})

def edit_view(request, id):

    if not request.user.is_authenticated or request.user.id != id:
        return redirect('/login')
    
    user = request.user
    
    if request.method == "POST":
        user.email = request.POST.get("email")
        if "photo" in request.FILES:
            if user.photo:
                user.photo.delete(save=False)
            user.photo = request.FILES["photo"]
        
        new_password = request.POST.get("password")
        if new_password:
            user.set_password(new_password)
        user.save()

        login(request, user)
        
        return redirect("core:recognize")

    return render(request, 'core/edit.html', {'user': user})
