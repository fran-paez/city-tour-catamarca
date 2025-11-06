from django.shortcuts import render,redirect

# Create your views here.
from .models import Parada
from .forms import ParadaForm

from .models import Recorrido
from .forms import RecorridoForm

from .models import Unidad
from .forms import UnidadForm

from .models import Itinerario
from .forms import ItinerarioForm


def lista_paradas(request):
    paradas = Parada.objects.all()
    return render(request, 'recorrido/lista_paradas.html', {'paradas': paradas})

def lista_recorridos(request):
    recorridos = Recorrido.objects.all()
    return render(request, 'recorrido/lista_recorridos.html', {'recorridos': recorridos})

def lista_itinerarios(request):
    itinerarios = Itinerario.objects.all().select_related('recorrido', 'unidad')
    return render(request, 'recorrido/lista_itinerarios.html', {'itinerarios': itinerarios})

def lista_unidades(request):
    unidades = Unidad.objects.all()
    return render(request, 'recorrido/lista_unidades.html', {'unidades': unidades})


def crear_parada(request):
    if request.method == 'POST':
        form = ParadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas') 
    else:
        form = ParadaForm()

    return render(request, 'recorrido/crear_parada.html', {'form': form})

def crear_recorrido(request):
    if request.method == 'POST':
        form = RecorridoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recorridos')
    else:
        form = RecorridoForm()
    return render(request, 'recorrido/crear_recorrido.html', {'form': form})


def agregar_unidad(request):
    if request.method == 'POST':
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades')
    else:
        form = UnidadForm()
    return render(request, 'recorrido/agregar_unidad.html', {'form': form})

def crear_itinerario(request):
    if request.method == 'POST':
        form = ItinerarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_itinerarios')
    else:
        form = ItinerarioForm()
    return render(request, 'recorrido/crear_itinerario.html', {'form': form})