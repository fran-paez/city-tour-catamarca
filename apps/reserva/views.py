from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from apps.recorrido.models import Parada
from apps.reserva.models import Notificacion, Reserva
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from apps.reserva.forms import NotificacionForm, ReservaForm
from django.db import transaction

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

# CRUD DE RESERVAS (solo turistas)

@login_required
def mis_reservas(request):
    """
    Muestra al turista un listado de sus propias reservas.
    (READ - List)
    """
    # 1. Seguridad de Rol
    if request.user.rol.nombre != 'TURISTA':
        return HttpResponseForbidden("Acceso denegado. Esta sección es solo para turistas.")

    # 2. Consulta: Filtra solo por el usuario logueado
    reservas = Reserva.objects.filter(
        turista=request.user
    ).order_by('-itinerario__fecha_itinerario')  # Mostrar las más próximas primero

    contexto = {
        'reservas': reservas
    }
    return render(request, 'reserva/mis_reservas.html', contexto)


@login_required()
@transaction.atomic  # <-- Transacción Atómica
def crear_reserva(request):
    """
    Muestra el formulario para crear una reserva y
    procesa la creación, descontando cupos.
    (CREATE)
    """
    if request.user.rol.nombre != 'TURISTA':
        return HttpResponseForbidden("Solo los turistas pueden crear reservas.")

    itinerario_id_inicial = request.GET.get('itinerario_id', None)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            itinerario = form.cleaned_data['itinerario']
            cantidad = form.cleaned_data['cantidad_asientos']

            # Combinamos fecha y hora para una comparación correcta
            itinerario_datetime = datetime.combine(itinerario.fecha_itinerario, itinerario.hora_itinerario)
            itinerario_datetime_aware = timezone.make_aware(itinerario_datetime, timezone.get_current_timezone())

            # Verificación de 1 hora de anticipación
            if itinerario_datetime_aware < timezone.now() + timedelta(hours=1):
                form.add_error('itinerario', 'No se puede realizar una reserva con menos de una hora de antelación al inicio del recorrido.')
            else:
                itinerario.cupos -= cantidad
                itinerario.save()

                reserva = form.save(commit=False)
                reserva.turista = request.user
                reserva.estado = 'C'
                reserva.save()

                return redirect('mis_reservas')
    else:
        form = ReservaForm(itinerario_id=itinerario_id_inicial)

    contexto = {
        'form': form,
        'titulo_pagina': 'Crear Nueva Reserva'
    }
    return render(request, 'reserva/crear_reserva.html', contexto)


@login_required
def detalle_reserva(request, pk):
    """
    Muestra el detalle de una reserva específica.
    (READ - Detail)
    """
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.user.rol.nombre != 'TURISTA':
        return HttpResponseForbidden("Acceso denegado.")

    if reserva.turista != request.user:
        return HttpResponseForbidden("No puedes ver una reserva que no es tuya.")

    contexto = {
        'reserva': reserva
    }
    return render(request, 'reserva/detalle_reserva.html', contexto)


@login_required
@transaction.atomic  # <-- Transacción Atómica
def cancelar_reserva(request, pk):
    """
    Permite a un turista cancelar una reserva.
    Restaura los cupos al itinerario.
    (DELETE / Update)
    """
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.user.rol.nombre != 'TURISTA' or reserva.turista != request.user:
        return HttpResponseForbidden("No puedes cancelar una reserva que no es tuya.")

    if reserva.estado == 'A':
        return redirect('mis_reservas')

    # Combinamos fecha y hora para una comparación correcta
    itinerario_datetime = datetime.combine(reserva.itinerario.fecha_itinerario, reserva.itinerario.hora_itinerario)
    itinerario_datetime_aware = timezone.make_aware(itinerario_datetime, timezone.get_current_timezone())

    # Verificación de 1 hora de anticipación
    puede_cancelar = itinerario_datetime_aware > timezone.now() + timedelta(hours=1)
    error_cancelacion = "No se puede cancelar una reserva con menos de una hora de antelación al inicio del recorrido." if not puede_cancelar else None

    if request.method == 'POST':
        if not puede_cancelar:
            return HttpResponseForbidden(error_cancelacion)
        
        itinerario = reserva.itinerario
        nuevos_cupos = itinerario.cupos + reserva.cantidad_asientos
        max_asientos_unidad = itinerario.unidad.cantidad_asientos

        if nuevos_cupos > max_asientos_unidad:
            itinerario.cupos = max_asientos_unidad
        else:
            itinerario.cupos = nuevos_cupos

        itinerario.save()

        reserva.estado = 'A'
        reserva.save()

        return redirect('mis_reservas')

    contexto = {
        'reserva': reserva,
        'puede_cancelar': puede_cancelar,
        'error_cancelacion': error_cancelacion
    }
    return render(request, 'reserva/cancelar_reserva.html', contexto)
