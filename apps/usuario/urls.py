# apps/usuario/urls.py

from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- URLs de Autenticación ---
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='usuario/login.html'  # Le decimos qué template usar
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # --- URLs de la App ---
    # Una nueva vista "home" para recibir al usuario logueado
    path('home/', views.home_view, name='home'),

    # --- URLs de Usuarios (CRUD) ---
    path('lista/', views.listar_usuarios, name='listar_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),

    # --- URLs de Roles (CRUD) ---
    path('roles/', views.listar_roles, name='listar_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),


]