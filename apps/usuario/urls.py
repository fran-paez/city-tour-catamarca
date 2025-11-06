# apps/usuario/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs para Roles
    # e.g., /usuario/roles/
    path('roles/', views.listar_roles, name='listar_roles'),

    # e.g., /usuario/roles/crear/
    path('roles/crear/', views.crear_rol, name='crear_rol'),
]