# apps/usuario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --- URLs para Usuarios ---
    path('', views.listar_usuarios, name='listar_usuarios'),

    path('crear/', views.crear_usuario, name='crear_usuario'),

    # --- URLs para Roles ---
    path('roles/', views.listar_roles, name='listar_roles'),

    path('roles/crear/', views.crear_rol, name='crear_rol'),
]