from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from apps.recorrido.models import Parada, Recorrido
from apps.reserva.models import Notificacion, Reserva
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from apps.reserva.forms import NotificacionForm, ReservaForm
from django.db import transaction
from django.contrib import messages

def index(request):
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')[:4]
    recorridos = Recorrido.objects.filter(estado='activo').order_by('nombre_recorrido')[:4]
    notificaciones_publicas = Notificacion.objects.filter(es_publica=True).order_by('-fecha_hora')[:5]
    contexto = {'notificaciones': notificaciones_publicas, 'paradas': paradas, 'recorridos': recorridos}
    return render(request, 'reserva/index.html', contexto)

def paradas_disponibles(request):
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')
    return render(request, 'reserva/paradas_disponibles.html', {'paradas': paradas})

def parada_detalles(request, parada_id):
    parada = get_object_or_404(Parada, id=parada_id)
    recorridos = parada.recorridos.filter(estado='activo')
    return render(request, 'reserva/parada_detalles.html', {'parada': parada, 'recorridos': recorridos})

def recorridos_activos(request):
    recorridos = Recorrido.objects.filter(estado='activo').order_by('nombre_recorrido')
    return render(request, 'reserva/recorridos_activos.html', {'recorridos': recorridos})

def recorrido_detalles(request, recorrido_id):
    recorrido = get_object_or_404(Recorrido, id=recorrido_id)
    itinerarios = recorrido.itinerarios.filter(fecha_itinerario__gte=timezone.now().date()).order_by('fecha_itinerario', 'hora_itinerario')
    contexto = {'recorrido': recorrido, 'itinerarios': itinerarios}
    return render(request, 'reserva/recorrido_detalles.html', contexto)

# --- CRUD de Reservas ---

@login_required
def mis_reservas(request):
    if request.user.rol.nombre != 'TURISTA':
        return HttpResponseForbidden("Acceso denegado.")
    reservas = Reserva.objects.filter(turista=request.user).order_by('-fecha_reserva')
    return render(request, 'reserva/mis_reservas.html', {'reservas': reservas})

@login_required
def crear_reserva(request):
    if request.user.rol.nombre != 'TURISTA':
        return HttpResponseForbidden("Solo los turistas pueden crear reservas.")
    
    itinerario_id_inicial = request.GET.get('itinerario_id', None)

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            itinerario = form.cleaned_data['itinerario']
            itinerario_datetime = datetime.combine(itinerario.fecha_itinerario, itinerario.hora_itinerario)
            itinerario_datetime_aware = timezone.make_aware(itinerario_datetime, timezone.get_current_timezone())

            if itinerario_datetime_aware < timezone.now() + timedelta(hours=1):
                form.add_error('itinerario', 'No se puede reservar con menos de una hora de antelación.')
            else:
                reserva = form.save(commit=False)
                reserva.turista = request.user
                reserva.estado = 'P'  # Se guarda como Pendiente
                reserva.save()
                messages.success(request, 'Tu prereserva ha sido guardada. Por favor, confírmala desde "Mis Reservas".')
                return redirect('mis_reservas')
    else:
        form = ReservaForm(itinerario_id=itinerario_id_inicial)

    return render(request, 'reserva/crear_reserva.html', {'form': form, 'titulo_pagina': 'Crear Nueva Reserva'})

@login_required
@transaction.atomic
def confirmar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if reserva.turista != request.user or reserva.estado != 'P':
        return HttpResponseForbidden("Acción no permitida.")

    itinerario = reserva.itinerario
    if itinerario.cupos < reserva.cantidad_asientos:
        messages.error(request, 'No hay suficientes asientos disponibles para confirmar esta reserva.')
        return redirect('detalle_reserva', pk=reserva.pk)

    itinerario.cupos -= reserva.cantidad_asientos
    itinerario.save()

    reserva.estado = 'C'  # Confirmada
    reserva.save()

    messages.success(request, '¡Tu reserva ha sido confirmada exitosamente!')
    return redirect('mis_reservas')

@login_required
def detalle_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if reserva.turista != request.user:
        return HttpResponseForbidden("No puedes ver una reserva que no es tuya.")
    return render(request, 'reserva/detalle_reserva.html', {'reserva': reserva})

@login_required
@transaction.atomic
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if reserva.turista != request.user or reserva.estado not in ['P', 'C']:
        return HttpResponseForbidden("No puedes cancelar esta reserva.")

    if request.method == 'POST':
        # Si la reserva estaba confirmada, devolvemos los cupos
        if reserva.estado == 'C':
            itinerario = reserva.itinerario
            itinerario_datetime = datetime.combine(itinerario.fecha_itinerario, itinerario.hora_itinerario)
            itinerario_datetime_aware = timezone.make_aware(itinerario_datetime, timezone.get_current_timezone())

            if itinerario_datetime_aware < timezone.now() + timedelta(hours=1):
                messages.error(request, "No se puede cancelar una reserva confirmada con menos de una hora de antelación.")
                return redirect('mis_reservas')
            
            itinerario.cupos += reserva.cantidad_asientos
            itinerario.save()

        reserva.estado = 'A'  # Cancelada
        reserva.save()
        messages.success(request, 'La reserva ha sido cancelada.')
        return redirect('mis_reservas')

    return render(request, 'reserva/cancelar_reserva.html', {'reserva': reserva})

# --- Vistas de Notificaciones (sin cambios) ---
@login_required
def listar_notificaciones(request):
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso.")
    notificaciones = Notificacion.objects.all()
    return render(request, 'reserva/panel_notificaciones.html', {'notificaciones': notificaciones})

@login_required
def crear_notificacion(request):
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso.")
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            notificacion = form.save(commit=False)
            notificacion.creado_por = request.user
            notificacion.save()
            return redirect('listar_notificaciones')
    else:
        form = NotificacionForm()
    return render(request, 'reserva/notificacion_form.html', {'form': form})

@login_required
def editar_notificacion(request, pk):
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso.")
    notificacion = get_object_or_404(Notificacion, pk=pk)
    if request.method == 'POST':
        form = NotificacionForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            return redirect('listar_notificaciones')
    else:
        form = NotificacionForm(instance=notificacion)
    return render(request, 'reserva/notificacion_form.html', {'form': form})

@login_required
def eliminar_notificacion(request, pk):
    if request.user.rol.nombre not in ['ADMINISTRADOR', 'OPERADOR']:
        return HttpResponseForbidden("No tienes permiso.")
    notificacion = get_object_or_404(Notificacion, pk=pk)
    if request.method == 'POST':
        notificacion.delete()
        return redirect('listar_notificaciones')
    return render(request, 'reserva/eliminar_notificacion.html', {'notificacion': notificacion})