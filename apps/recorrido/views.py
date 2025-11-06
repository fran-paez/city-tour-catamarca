from django.shortcuts import render,redirect

# Create your views here.
from .models import Parada
from .forms import ParadaForm

from .models import Recorrido
from .forms import RecorridoForm


def crear_parada(request):
    if request.method == 'POST':
        form = ParadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas') 
    else:
        form = ParadaForm()

    return render(request, 'recorrido/crear_parada.html', {'form': form})

def lista_paradas(request):
    paradas = Parada.objects.all()
    return render(request, 'recorrido/lista_paradas.html', {'paradas': paradas})



def lista_recorridos(request):
    recorridos = Recorrido.objects.all()
    return render(request, 'recorrido/lista_recorridos.html', {'recorridos': recorridos})

def crear_recorrido(request):
    if request.method == 'POST':
        form = RecorridoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recorridos')
    else:
        form = RecorridoForm()
    return render(request, 'recorrido/crear_recorrido.html', {'form': form})
