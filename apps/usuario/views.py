from django.shortcuts import render, redirect, get_object_or_404
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden # Para responder "Acceso Denegado"
from .models import Rol, Usuario
from .forms import RolForm, UsuarioCreationForm, UsuarioChangeForm
# Create your views here.

# --- Vistas para ROL ---

@login_required
def listar_roles(request):
    """
    Vista para listar todos los roles existentes.
    """

    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

    roles = Rol.objects.all()

    contexto = {
        'roles': roles
    }

    return render(request, 'usuario/listar_roles.html', contexto)

@login_required
def crear_rol(request):
    """
    Vista para crear un nuevo Rol usando el RolForm.
    """

    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

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


@login_required
def editar_rol(request, rol_id):
    """
    Vista para editar un Rol existente.
    """
    # 1. Seguridad de Acceso: Solo Admins pueden editar roles.
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

    rol_a_editar = get_object_or_404(Rol, id=rol_id)

    # 2. Seguridad de Regla de Negocio: No se puede editar el rol ADMIN.
    if rol_a_editar.nombre == 'ADMINISTRADOR':
        return redirect('listar_roles')

    if request.method == 'POST':
        form = RolForm(request.POST, instance=rol_a_editar)
        if form.is_valid():
            # El método save() del MODELO se encargará de
            # guardar el nombre en MAYÚSCULAS automáticamente.
            form.save()
            return redirect('listar_roles')
    else:
        form = RolForm(instance=rol_a_editar)

    contexto = {
        'form': form,
        'rol': rol_a_editar
    }
    return render(request, 'usuario/editar_rol.html', contexto)


@login_required
def eliminar_rol(request, rol_id):
    """
    Vista para eliminar un Rol.
    """
    # 1. Seguridad de Acceso: Solo Admins.
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

    rol_a_eliminar = get_object_or_404(Rol, id=rol_id)

    # 2. Seguridad de Regla de Negocio: No se puede eliminar el rol ADMIN.
    if rol_a_eliminar.nombre == 'ADMINISTRADOR':
        return redirect('listar_roles')

    # Solo eliminamos por POST (por seguridad)
    if request.method == 'POST':
        rol_a_eliminar.delete()
        return redirect('listar_roles')

    # Si es GET, mostramos confirmación
    contexto = {
        'rol': rol_a_eliminar
    }
    return render(request, 'usuario/eliminar_rol.html', contexto)

# --- VISTAS PARA USUARIO ---
@login_required
def listar_usuarios(request):
    """
    Vista para listar todos los usuarios del sistema.
    """
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

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
            return redirect('login')
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
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para acceder a esta sección o no puedes realizar esta accion con tu propio usuario.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario_a_editar, request=request)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario_a_editar, request=request)

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
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para acceder a esta sección.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)

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
