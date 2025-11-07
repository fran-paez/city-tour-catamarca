from django.shortcuts import render, redirect
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm
from django.contrib.auth.decorators import login_required
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm
# Create your views here.

# --- Vistas para ROL ---

def listar_roles(request):
    """
    Vista para listar todos los roles existentes.
    """
    roles = Rol.objects.all()

    contexto = {
        'roles': roles
    }

    return render(request, 'usuario/listar_roles.html', contexto)


def crear_rol(request):
    """
    Vista para crear un nuevo Rol usando el RolForm.
    """
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_roles')
    else:
        form = RolForm()

    contexto = {
        'form': form
    }

    return render(request, 'usuario/crear_rol.html', contexto)


# --- VISTAS PARA USUARIO ---

def listar_usuarios(request):
    """
    Vista para listar todos los usuarios del sistema.
    """
    usuarios = Usuario.objects.all()
    contexto = {
        'usuarios': usuarios
    }
    return render(request, 'usuario/listar_usuarios.html', contexto)


def crear_usuario(request):
    """
    Vista para crear un nuevo Usuario usando el UsuarioCreationForm.
    """
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigimos a la lista de usuarios
            return redirect('listar_usuarios')
    else:
        # Si es GET, creamos el formulario vacío
        form = UsuarioCreationForm()

    contexto = {
        'form': form
    }
    return render(request, 'usuario/crear_usuario.html', contexto)

# --- VISTA HOME ---
@login_required
def home_view(request):
    """
    Página de inicio que solo pueden ver los usuarios logueados.
    """
    return render(request, 'usuario/home.html')