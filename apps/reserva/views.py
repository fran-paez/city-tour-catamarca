from django.shortcuts import render
from apps.recorrido.models import Parada
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
import os


def index(request):
    # Obtener solo las primeras 4 paradas visibles
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')[:4]
    return render(request, 'reserva/index.html', {'paradas': paradas})

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
