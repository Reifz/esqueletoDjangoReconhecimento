import json
import base64
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os
from django.core.files.base import ContentFile
import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from core.forms import UserRegisterForm
from .models import LogAcesso, Usuario

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o usuário apenas na sessão
            request.session.flush()  # Limpa sessão anterior
            
            # Armazenar dados na sessão
            user_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'nivel_acesso': form.cleaned_data.get('nivel_acesso', Usuario.ACCESS_LEVEL_1),
            }
            
            # Armazenar a foto como base64 na sessão
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                photo_data = base64.b64encode(photo_file.read()).decode('utf-8')
                user_data['photo_data'] = photo_data
                user_data['photo_name'] = photo_file.name
            
            request.session['user_data'] = user_data
            request.session['face_verified'] = False
            request.session['verification_time'] = 0
            
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

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
            # Armazenar dados do usuário na sessão
            request.session['user_data'] = {
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'photo_url': user.photo.url if user.photo else None,
                'nivel_acesso': user.nivel_acesso,
            }
            
            # Resetar verificação facial
            request.session['face_verified'] = False
            request.session['verification_time'] = 0
            
            return redirect("core:recognize")
        else:
            error = "Credenciais inválidas"

    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    if request.user.is_authenticated:
        request.user.is_active = False
        logout(request)
    
    # Limpar sessão
    request.session.flush()
    return redirect('core:login')

def recognize_view(request):
    if request.method == 'POST':
        temp_img_path = None
        temp_ref_path = None
        try:
            # Verificar se existem dados do usuário na sessão
            if 'user_data' not in request.session:
                return JsonResponse({'error': 'Dados do usuário não encontrados. Faça o registro ou login novamente.'}, status=400)

            user_data = request.session['user_data']
            
            # Decodificar a imagem da câmera
            data = json.loads(request.body)
            image_data = data['image']
            format, imgstr = image_data.split(';base64,') 
            img_data = base64.b64decode(imgstr)
            
            # Converter para CV2
            nparr = np.frombuffer(img_data, np.uint8)
            img_captured = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Criar arquivo temporário para imagem capturada
            fd, temp_img_path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)
            cv2.imwrite(temp_img_path, img_captured)
            
            # Preparar imagem de referência baseado no tipo de usuário
            if 'photo_data' in user_data:
                # CASO 1: Usuário novo (registro) - foto está na sessão
                photo_data = base64.b64decode(user_data['photo_data'])
                fd, temp_ref_path = tempfile.mkstemp(suffix='.jpg')
                os.close(fd)
                with open(temp_ref_path, 'wb') as f:
                    f.write(photo_data)
                reference_image_path = temp_ref_path
            else:
                # CASO 2: Usuário existente (login) - foto está no banco
                user = Usuario.objects.get(id=user_data['user_id'])
                reference_image_path = user.photo.path

            # Verificar rosto
            print("Realizando verificação facial...")
            result = DeepFace.verify(
                img1_path=str(reference_image_path),
                img2_path=temp_img_path,
                model_name='VGG-Face',
                enforce_detection=False
            )
            print("Verificação concluída:", result['verified'])

            # Processar resultado
            if result['verified']:
                # Verificação bem-sucedida
                
                # Se for usuário novo, criar no banco
                if 'photo_data' in user_data:
                    user = Usuario(
                        email=user_data['email'],
                        name=user_data['name'],
                        nivel_acesso=user_data['nivel_acesso']
                    )
                    user.set_password(user_data['password'])
                    
                    # Salvar a foto
                    photo_data = base64.b64decode(user_data['photo_data'])
                    photo_file = ContentFile(photo_data, name=user_data['photo_name'])
                    user.photo = photo_file
                    
                    user.save()
                    
                    # Fazer login
                    login(request, user)
                    
                    # Atualizar dados na sessão
                    request.session['user_data'] = {
                        'user_id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'photo_url': user.photo.url,
                        'nivel_acesso': user.nivel_acesso,
                    }
                
                # Atualizar verificação na sessão
                request.session['face_verified'] = True
                request.session['verification_time'] = time.time()
                
                # Registrar log
                log_user = user if 'user' in locals() else Usuario.objects.get(id=user_data['user_id'])
                LogAcesso.objects.create(
                    usuario=log_user,
                    result=LogAcesso.RESULT_APPROVED
                )

                return JsonResponse({
                    'verified': True, 
                    'redirect_url': reverse('core:home')
                })
            else:
                # Verificação falhou
                if 'user_id' in user_data:
                    log_user = Usuario.objects.get(id=user_data['user_id'])
                    LogAcesso.objects.create(
                        usuario=log_user,
                        result=LogAcesso.RESULT_DENIED
                    )
                
                return JsonResponse({
                    'verified': False, 
                    'distance': result['distance']
                })
                
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            # Limpar arquivos temporários
            for temp_path in [temp_img_path, temp_ref_path]:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # GET request - mostrar página de reconhecimento
    return render(request, 'core/recognize.html')

def home_view(request):
    # Verificar se usuário está autenticado E com face verificada
    if not request.user.is_authenticated:
        return redirect('/login')
    
    # Verificar verificação facial na sessão
    face_verified = request.session.get('face_verified', False)
    verification_time = request.session.get('verification_time', 0)
    
    if not face_verified or time.time() - verification_time > 300:  # 5 minutos
        return redirect('core:recognize')
    
    return render(request, 'core/home.html', {'user': request.user})

def redirect_home(request, exception=None):
    return redirect('/')

def edit_view(request, id):
    if not request.user.is_authenticated or request.user.id != id:
        return redirect('/login')
    
    user = request.user
    
    if request.method == "POST":
        user.email = request.POST.get("email")
        user.name = request.POST.get("name")
        user.nivel_acesso = request.POST.get("nivel_acesso", Usuario.ACCESS_LEVEL_1)
        
        if "photo" in request.FILES:
            if user.photo:
                user.photo.delete(save=False)
            user.photo = request.FILES["photo"]
            # Resetar verificação facial
            request.session['face_verified'] = False
        
        new_password = request.POST.get("password")
        if new_password:
            user.set_password(new_password)
        
        user.save()

        # Atualizar sessão se a senha mudou
        if new_password:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
        else:
            login(request, user)
        
        # Atualizar dados na sessão
        request.session['user_data'] = {
            'user_id': user.id,
            'email': user.email,
            'name': user.name,
            'photo_url': user.photo.url,
            'nivel_acesso': user.nivel_acesso,
        }
        
        # Se a foto foi alterada, exigir nova verificação
        if "photo" in request.FILES:
            return redirect("core:recognize")
        else:
            return redirect("core:home")

    return render(request, 'core/edit.html', {'user': user})