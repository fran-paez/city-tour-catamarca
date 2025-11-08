from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
# Create your views here.

@login_required
def dashboard_informes(request):
    """
    Muestra la página principal de informes (el dashboard)
    solo a los administradores.
    """
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    return render(request, 'informe/dashboard.html')


@login_required
def generar_informe_pasajeros_fechas(request):
    """
    Recibe las fechas y el formato desde el dashboard
    """
    if request.user.rol.nombre != 'ADMINISTRADOR':
        return HttpResponseForbidden("Acceso denegado")

    # 2. Obtener datos de la URL (porque usamos method="GET")
    fecha_inicio = request.GET.get('fecha_inicio', None)
    fecha_fin = request.GET.get('fecha_fin', None)
    formato = request.GET.get('formato', 'pdf')  # pdf por defecto

    # 3. Validar que las fechas existan
    if not (fecha_inicio and fecha_fin):
        # Si no mandó fechas, lo regresamos al dashboard
        return redirect('dashboard_informes')

        # 4. (FUTURO) Aquí harías la consulta a la BD
    # reservas = Reserva.objects.filter(
    #     itinerario__fecha__range=[fecha_inicio, fecha_fin]
    # )
    # total_pasajeros = ...

    # 5. (FUTURO) Aquí llamarías a la función que genera el archivo
    # if formato == 'pdf':
    #    return generar_pdf(reservas)

    # --- POR AHORA: Devolvemos un simple HttResponse para confirmar ---
    # Esto nos permite probar que la vista recibe los datos
    # antes de meternos con la lógica de generar archivos.
    respuesta = (
        f"<h1>Recibido (Prueba)</h1>"
        f"<p>Generando reporte en formato: <b>{formato.upper()}</b></p>"
        f"<p>Desde: <b>{fecha_inicio}</b></p>"
        f"<p>Hasta: <b>{fecha_fin}</b></p>"
        f"<p><i>(Aquí se generaría el archivo...)</i></p>"
    )
    return HttpResponse(respuesta)