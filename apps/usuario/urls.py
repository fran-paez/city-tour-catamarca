# apps/usuario/urls.py

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

    # --- URLs de Usuarios (CRUD) ---
    path('lista/', views.listar_usuarios, name='listar_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),

# --- URLs PARA EDITAR Y ELIMINAR usuarios ---
    # e.g., /usuario/editar/1/
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    # e.g., /usuario/eliminar/1/
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # --- URLs de Roles (CRUD) ---
    path('roles/', views.listar_roles, name='listar_roles'),
    path('roles/crear/', views.crear_rol, name='crear_rol'),

# e.g., /usuario/roles/editar/1/
    path('roles/editar/<int:rol_id>/', views.editar_rol, name='editar_rol'),
    # e.g., /usuario/roles/eliminar/1/
    path('roles/eliminar/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),

]