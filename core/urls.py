from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recognize/', views.recognize_view, name='recognize'),
    path('cofre/', views.cofre_view, name='cofre')
]