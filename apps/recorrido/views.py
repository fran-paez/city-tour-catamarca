from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Parada, Recorrido, Unidad, Itinerario
from .forms import ParadaForm, RecorridoForm, UnidadForm, ItinerarioForm

# Vistas de Listado
@login_required
def lista_paradas(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para visitar esta seccion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    paradas = Parada.objects.all()
    return render(request, 'recorrido/lista_paradas.html', {'paradas': paradas})

@login_required
def lista_recorridos(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para visitar esta seccion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    recorridos = Recorrido.objects.all()
    return render(request, 'recorrido/lista_recorridos.html', {'recorridos': recorridos})

@login_required
def lista_itinerarios(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para visitar esta seccion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    itinerarios = Itinerario.objects.all().select_related('recorrido', 'unidad')
    return render(request, 'recorrido/lista_itinerarios.html', {'itinerarios': itinerarios})

@login_required
def lista_unidades(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Acceso Denegado',
            'error_mensaje': 'No tienes permisos para visitar esta seccion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    unidades = Unidad.objects.all()
    return render(request, 'recorrido/lista_unidades.html', {'unidades': unidades})

# Vistas de Creación
@login_required
def crear_parada(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    if request.method == 'POST':
        form = ParadaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas')
    else:
        form = ParadaForm()
    return render(request, 'recorrido/crear_parada.html', {'form': form})

@login_required
def crear_recorrido(request):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
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
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
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
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    if request.method == 'POST':
        form = ItinerarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_itinerarios')
    else:
        form = ItinerarioForm()
    return render(request, 'recorrido/crear_itinerario.html', {'form': form})

# Vistas de Edición
@login_required
def editar_parada(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    parada = get_object_or_404(Parada, pk=pk)
    if request.method == 'POST':
        form = ParadaForm(request.POST, request.FILES, instance=parada)
        if form.is_valid():
            form.save()
            return redirect('lista_paradas')
    else:
        form = ParadaForm(instance=parada)
    return render(request, 'recorrido/editar_parada.html', {'form': form})

@login_required
def editar_recorrido(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    recorrido = get_object_or_404(Recorrido, pk=pk)
    if request.method == 'POST':
        form = RecorridoForm(request.POST, instance=recorrido)
        if form.is_valid():
            form.save()
            return redirect('lista_recorridos')
    else:
        form = RecorridoForm(instance=recorrido)
    return render(request, 'recorrido/editar_recorrido.html', {'form': form})

@login_required
def editar_unidad(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    unidad = get_object_or_404(Unidad, pk=pk)
    if request.method == 'POST':
        form = UnidadForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('lista_unidades')
    else:
        form = UnidadForm(instance=unidad)
    return render(request, 'recorrido/editar_unidad.html', {'form': form})

@login_required
def editar_itinerario(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    itinerario = get_object_or_404(Itinerario, pk=pk)
    if request.method == 'POST':
        form = ItinerarioForm(request.POST, instance=itinerario)
        if form.is_valid():
            form.save()
            return redirect('lista_itinerarios')
    else:
        form = ItinerarioForm(instance=itinerario)
    return render(request, 'recorrido/editar_itinerario.html', {'form': form})

# Vistas de Eliminación
@login_required
def eliminar_parada(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    parada = get_object_or_404(Parada, pk=pk)
    if request.method == 'POST':
        parada.delete()
        return redirect('lista_paradas')
    return render(request, 'recorrido/eliminar_parada.html', {'parada': parada})

@login_required
def eliminar_recorrido(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    recorrido = get_object_or_404(Recorrido, pk=pk)
    if request.method == 'POST':
        recorrido.delete()
        return redirect('lista_recorridos')
    return render(request, 'recorrido/eliminar_recorrido.html', {'recorrido': recorrido})

@login_required
def eliminar_unidad(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    unidad = get_object_or_404(Unidad, pk=pk)
    if request.method == 'POST':
        unidad.delete()
        return redirect('lista_unidades')
    return render(request, 'recorrido/eliminar_unidad.html', {'unidad': unidad})

@login_required
def eliminar_itinerario(request, pk):
    if request.user.rol.nombre != 'ADMINISTRADOR':
        contexto_error = {
            'error_titulo': 'Accion Denegada',
            'error_mensaje': 'No tienes permisos para realizar esta accion.'
        }
        # Renderizamos el template y pasamos el código 403
        return render(request, 'reserva/error_permiso.html', contexto_error, status=403)
    itinerario = get_object_or_404(Itinerario, pk=pk)
    if request.method == 'POST':
        itinerario.delete()
        return redirect('lista_itinerarios')
    return render(request, 'recorrido/eliminar_itinerario.html', {'itinerario': itinerario})
