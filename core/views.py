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



def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():

            request.session['pending_register'] = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'name': form.cleaned_data['name'],
                'photo': form.cleaned_data['photo'].name,  
            }

            
            photo = form.cleaned_data['photo']
            temp_path = os.path.join(tempfile.gettempdir(), photo.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)

            request.session['pending_register_photo'] = temp_path

            return redirect('core:recognize')
        else:
            return render(request, 'core/register.html', {'form': form})

    else:
        form = UserRegisterForm()
        return render(request, 'core/register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = Usuario.objects.get(email=email)
            if user.verify_password(password): #valida a senha do usuário
                request.session["pending_user_id"] = user.id
                return redirect("core:recognize")
            else:
                error = "Senha incorreta"
        except Usuario.DoesNotExist:
            error = "Usuário não encontrado"
    return render(request, "core/login.html", {"error": error})

def logout_view(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect('core:login')

def recognize_view(request):
    if request.method == 'POST':
        temp_img_path = None
        try:

            pending_data = request.session.get('pending_register')
            pending_photo = request.session.get('pending_register_photo')

            if not pending_data or not pending_photo:
                return JsonResponse({'error': 'Nenhum registro pendente'}, status=400)

            data = json.loads(request.body)
            image_data = data['image']
            format, imgstr = image_data.split(';base64,') 
            img_data = base64.b64decode(imgstr)

            nparr = np.frombuffer(img_data, np.uint8)
            img_captured = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            fd, temp_img_path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)
            cv2.imwrite(temp_img_path, img_captured)

            # Compara com a foto enviada no cadastro
            result = DeepFace.verify(
                img1_path=str(pending_photo),
                img2_path=temp_img_path,
                model_name='VGG-Face',
                enforce_detection=False
            )

            if result['verified']:

                user = Usuario(
                    email=pending_data['email'],
                    name=pending_data['name'],
                )
                user.set_password(pending_data['password'])
                user.photo.name = pending_data['photo']  # salva a foto original
                user.save()

                LogAcesso.objects.create(usuario=user, result=LogAcesso.RESULT_APPROVED)

                request.session['user_id'] = user.id
                request.session.pop('pending_register', None)
                request.session.pop('pending_register_photo', None)

                return JsonResponse({
                    'verified': True,
                    'redirect_url': reverse('core:home')
                })
            else:
                return JsonResponse({
                    'verified': False,
                    'distance': result['distance']
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            if temp_img_path and os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
    return render(request, 'core/recognize.html')



def home_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/login')

    user = Usuario.objects.get(id=user_id)

    return render(request, 'core/home.html', {'user': user})

def edit_view(request, id):

    user = Usuario.objects.get(id=id)

    if not id:
        return redirect('/login')
    
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
        return redirect("core:recognize")

    return render(request, 'core/edit.html', {'user': user})
