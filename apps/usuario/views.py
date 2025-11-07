from django.shortcuts import render, redirect, get_object_or_404
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden # Para responder "Acceso Denegado"
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm, UsuarioChangeForm
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

@login_required
def editar_usuario(request, usuario_id):
    """
    Vista para editar un usuario existente.
    Aplica lógica de seguridad A5.
    """
    # Obtenemos el usuario que se quiere editar
    usuario_a_editar = get_object_or_404(Usuario, id=usuario_id)

    es_admin = request.user.rol.nombre == 'ADMINISTRADOR'
    es_el_mismo_usuario = request.user.id == usuario_a_editar.id

    if not (es_admin or es_el_mismo_usuario):
        # Si no es admin Y no es él mismo, le negamos el acceso.
        return HttpResponseForbidden("No tienes permiso para editar este usuario.")

    # --- Lógica del formulario ---
    if request.method == 'POST':
        # Pasamos la instancia para que el formulario sepa QUÉ usuario actualizar
        form = UsuarioChangeForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        # Si es GET, creamos el formulario relleno con los datos del usuario
        form = UsuarioChangeForm(instance=usuario_a_editar)

    contexto = {
        'form': form,
        'usuario_editado': usuario_a_editar
    }
    return render(request, 'usuario/editar_usuario.html', contexto)


@login_required
def eliminar_usuario(request, usuario_id):
    """
    Vista para eliminar un usuario.
    Solo accesible por Administradores.
    """
    usuario_a_eliminar = get_object_or_404(Usuario, id=usuario_id)

    es_admin = request.user.rol.nombre == 'ADMINISTRADOR'

    if not es_admin:
        # Solo los administradores pueden eliminar usuarios.
        return HttpResponseForbidden("No tienes permiso para eliminar usuarios.")

    # Evita que un admin se elimine a sí mismo
    if request.user.id == usuario_a_eliminar.id:
        return redirect('listar_usuarios')

    # Importante: El borrado debe ser por POST por seguridad (como el logout)
    if request.method == 'POST':
        usuario_a_eliminar.delete()
        return redirect('listar_usuarios')

    # Si es GET, mostramos una página de confirmación
    contexto = {
        'usuario': usuario_a_eliminar
    }
    return render(request, 'usuario/eliminar_usuario.html', contexto)

# --- VISTA HOME ---
@login_required
def home_view(request):
    """
    Página de inicio que solo pueden ver los usuarios logueados.
    """
    return render(request, 'usuario/home.html')