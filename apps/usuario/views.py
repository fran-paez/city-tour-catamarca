from django.shortcuts import render, redirect
from .models import Rol
from .forms import RolForm

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