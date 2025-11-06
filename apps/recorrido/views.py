from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ParadaForm


def crear_parada(request):
    if request.method == 'POST':
        form = ParadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas')  # puedes redirigir a la lista de paradas
    else:
        form = ParadaForm()

    return render(request, 'recorrido/crear_parada.html', {'form': form})

from .models import Parada

def lista_paradas(request):
    paradas = Parada.objects.all()
    return render(request, 'recorrido/lista_paradas.html', {'paradas': paradas})
