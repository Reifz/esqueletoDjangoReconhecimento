from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('recognize/', views.recognize_view, name='recognize'),
    path('home/', views.home_view, name='home'),
]
