from django.contrib.auth.decorators import login_required
from apps.recorrido.models import Parada
from apps.reserva.models import Notificacion
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from apps.reserva.forms import NotificacionForm

def index(request):
    # Obtener solo las primeras 4 paradas visibles
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')[:4]

    # Buscamos las 5 notificaciones más nuevas
    # que estén marcadas como 'es_publica'.
    notificaciones_publicas = Notificacion.objects.filter(
        es_publica=True
    ).order_by('-fecha_hora')[:5]

    contexto = {
        'notificaciones': notificaciones_publicas,
        'paradas': paradas
    }
    return render(request, 'reserva/index.html', contexto)

def paradas_disponibles(request):
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')
    return render(request, 'reserva/index.html', {'paradas': paradas})


def parada_detalles(request, parada_id):
    parada = get_object_or_404(Parada, id=parada_id)
    # Obtener todos los recorridos que incluyen esta parada y están activos
    recorridos = parada.recorridos.filter(estado='activo')
    return render(request, 'reserva/parada_detalles.html', {
        'parada': parada,
        'recorridos': recorridos
    })


### CREAR RESERVA
# @login_required
# def crear_reserva(request):
#     if request.user.rol.nombre != 'TURISTA':
#         return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
#     paradas = Parada.objects.all()
#     return render(request, 'recorrido/crear_reserva.html', {'paradas': paradas})

def paradas_disponibles(request):
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')  # opcional order_by
    return render(request, 'reserva/paradas_disponibles.html', {'paradas': paradas})

# CRUD para notificaciones

@login_required
def listar_notificaciones(request):
    """
    Lista todas las notificaciones creadas.
    Solo para Operadores y Administradores.
    """
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    notificaciones = Notificacion.objects.all().order_by('-fecha_hora')
    contexto = {
        'notificaciones': notificaciones
    }
    return render(request, 'reserva/panel_notificaciones.html', contexto)


@login_required
def crear_notificacion(request):
    """
    Crea una nueva notificación.
    Guarda automáticamente quién la creó.
    """
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            # asignamos el creador antes de guardar
            notificacion = form.save(commit=False)
            notificacion.creado_por = request.user
            notificacion.save()
            return redirect('listar_notificaciones')
    else:
        form = NotificacionForm()

    contexto = {
        'form': form,
        'titulo_pagina': 'Crear Notificación'
    }
    return render(request, 'reserva/notificacion_form.html', contexto)


@login_required
def editar_notificacion(request, pk):
    """
    Edita una notificación existente.
    """
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    notificacion = get_object_or_404(Notificacion, pk=pk)

    if request.method == 'POST':
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()  # 'creado_por' ya estaba asignado
            return redirect('listar_notificaciones')
    else:
        form = NotificacionForm(instance=notificacion)

    contexto = {
        'form': form,
        'titulo_pagina': 'Editar Notificación'
    }
    return render(request, 'reserva/notificacion_form.html', contexto)


@login_required
def eliminar_notificacion(request, pk):
    """
    Muestra confirmación y elimina una notificación.
    """
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    notificacion = get_object_or_404(Notificacion, pk=pk)

    if request.method == 'POST':
        notificacion.delete()
        return redirect('listar_notificaciones')

    contexto = {
        'notificacion': notificacion
    }
    return render(request, 'reserva/eliminar_notificacion.html', contexto)