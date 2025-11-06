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


from django.shortcuts import render, redirect

from .models import Recorrido
from .forms import RecorridoForm
from django.shortcuts import render, redirect
#
# def crear_recorrido(request):
#     if request.method == 'POST':
#         form = RecorridoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('lista_recorridos')
#     else:
#         form = RecorridoForm()
#     return render(request, 'recorrido/crear_recorrido.html', {'form': form})


def lista_recorridos(request):
    recorridos = Recorrido.objects.all()
    return render(request, 'recorrido/lista_recorridos.html', {'recorridos': recorridos})


def crear_recorrido(request):
    # print("Llegamos a la vista crear_recorrido")  # línea de debug
    if request.method == 'POST':
        form = RecorridoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recorridos')
    else:
        form = RecorridoForm()
    print("Form generado:", form)  # debug para ver si se crea
    return render(request, 'recorrido/crear_recorrido.html', {'form': form})
