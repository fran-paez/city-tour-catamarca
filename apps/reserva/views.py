from django.shortcuts import render
from apps.recorrido.models import Parada

def index(request):
    paradas = Parada.objects.filter(visibilidad_pagina=True).order_by('nombre')  # opcional order_by
    return render(request, 'reserva/index.html', {'paradas': paradas})