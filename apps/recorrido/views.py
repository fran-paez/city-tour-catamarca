from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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


@login_required
def lista_paradas(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    paradas = Parada.objects.all()
    return render(request, 'recorrido/lista_paradas.html', {'paradas': paradas})

@login_required
def lista_recorridos(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    recorridos = Recorrido.objects.all()
    return render(request, 'recorrido/lista_recorridos.html', {'recorridos': recorridos})

@login_required
def lista_itinerarios(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    itinerarios = Itinerario.objects.all().select_related('recorrido', 'unidad')
    return render(request, 'recorrido/lista_itinerarios.html', {'itinerarios': itinerarios})

@login_required
def lista_unidades(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    unidades = Unidad.objects.all()
    return render(request, 'recorrido/lista_unidades.html', {'unidades': unidades})

@login_required
def crear_parada(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    if request.method == 'POST':
        form = ParadaForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas') 
    else:
        form = ParadaForm()

    return render(request, 'recorrido/crear_parada.html', {'form': form})

@login_required
def crear_recorrido(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    if request.method == 'POST':
        form = RecorridoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_recorridos')
    else:
        form = RecorridoForm()
    return render(request, 'recorrido/crear_recorrido.html', {'form': form})

@login_required
def agregar_unidad(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    if request.method == 'POST':
        form = UnidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades')
    else:
        form = UnidadForm()
    return render(request, 'recorrido/agregar_unidad.html', {'form': form})

@login_required
def crear_itinerario(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    if request.method == 'POST':
        form = ItinerarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_itinerarios')
    else:
        form = ItinerarioForm()
    return render(request, 'recorrido/crear_itinerario.html', {'form': form})

def pagina_principal(request):
    """
    Esta es la PÁGINA PRINCIPAL PÚBLICA.
    Cualquiera (logueado o no) puede verla.
    """
    # Cuando tengas los modelos:
    # recorridos = Recorrido.objects.filter(activo=True)

    contexto = {
        # 'recorridos': recorridos
    }

    # Necesitarás crear este template:
    return render(request, 'recorrido/pagina_principal.html', contexto)