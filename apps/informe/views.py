from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from apps.reserva.models import Reserva

# --- importaciones para formato CSV
import csv
import datetime

# --- importaciones para formato PDF ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 # Para el tamaño de hoja
from reportlab.lib import colors
from reportlab.lib.units import cm # Para usar centímetros

# --- Importaciones para Excel ---
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
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
    fecha_inicio_str = request.GET.get('fecha_inicio', None)
    fecha_fin_str = request.GET.get('fecha_fin', None)
    formato = request.GET.get('formato', 'pdf')  # pdf por defecto

    # 3. Validar que las fechas existan
    if not (fecha_inicio_str and fecha_fin_str):
        # Si no mandó fechas, lo regresamos al dashboard
        return redirect('dashboard_informes')

    # 3. Convertir las fechas de texto a objetos 'date'
    try:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Fechas inválidas. Use el formato AAAA-MM-DD.")

    # si la fecha inicio es posterior a la fecha de fin, informar error
    if fecha_inicio > fecha_fin:
        return HttpResponse(
            "Error: La 'Fecha de Inicio' no puede ser posterior a la 'Fecha de Fin'.",
            status=400
        )

    # 4. Obtener los datos de la BD (Consulta única)
    # Consultamos el modelo 'Reserva' directamente.
    reservas = Reserva.objects.filter(
        itinerario__fecha_itinerario__range=[fecha_inicio, fecha_fin],
        # Usamos el campo 'fecha_itinerario' del modelo Itinerario
        estado='C'  # Solo confirmadas
    ).select_related(
'turista',
    'itinerario__recorrido'  # Seguimos la relación anidada
    ).order_by('itinerario__fecha_itinerario')  # Ordenamos por l

    # 5. Calcular el total de pasajeros
    total_pasajeros = 0
    for r in reservas:
        total_pasajeros += r.cantidad_asientos

    # --- LÓGICA PARA CSV (Sin cambios) ---
    if formato == 'csv':
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = f'attachment; filename="reporte_pasajeros_{fecha_inicio_str}_al_{fecha_fin_str}.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID Reserva', 'Fecha Viaje', 'Recorrido', 'Turista', 'Asientos'])

        for reserva in reservas:
            writer.writerow([
                reserva.id,
                reserva.itinerario.fecha_itinerario,
                reserva.itinerario.recorrido.nombre_recorrido,
                reserva.turista.get_full_name(),
                reserva.cantidad_asientos
            ])

        writer.writerow([])
        writer.writerow(['Total de Pasajeros:', total_pasajeros])
        return response

        # --- ¡NUEVA LÓGICA PARA PDF! ---
    elif formato == 'pdf':
        # 1. Crear la respuesta HTTP con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'] = f'attachment; filename="reporte_pasajeros_{fecha_inicio_str}_al_{fecha_fin_str}.pdf"'

        # 2. Crear el "lienzo" (Canvas) de ReportLab
        # Usamos A4 y le pasamos la 'response' como el archivo donde "dibujar"
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4  # Obtenemos el ancho y alto
        # 3. Definir la posición inicial (Y)
        # ReportLab dibuja desde abajo-izquierda (0,0)
        # Empezamos a dibujar cerca de la parte de arriba
        y = height - (2 * cm)  # Margen superior de 2 cm
        x = 2 * cm  # Margen izquierdo de 2 cm

        # 4. Dibujar el Título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(x, y, "Reporte de Pasajeros por Fecha")
        y -= 0.5 * cm  # Bajar medio cm
        p.line(x, y, width - (2 * cm), y)  # Dibujar una línea
        y -= 1 * cm  # Bajar 1 cm

        # 5. Dibujar los detalles del reporte
        p.setFont("Helvetica", 12)
        p.drawString(x, y, f"Período: {fecha_inicio_str} al {fecha_fin_str}")
        y -= 1 * cm  # Bajar 1 cm

        # 6. Dibujar los encabezados de la tabla
        p.setFont("Helvetica-Bold", 11)
        p.drawString(x, y, "Fecha Viaje")
        p.drawString(x + (4 * cm), y, "Recorrido")
        p.drawString(x + (10 * cm), y, "Turista")
        p.drawString(x + (14 * cm), y, "Asientos")
        y -= 0.5 * cm  # Bajar medio cm

        # 7. Dibujar las filas de datos
        p.setFont("Helvetica", 10)
        for reserva in reservas:
            p.drawString(x, y, str(reserva.itinerario.fecha_itinerario))
            p.drawString(x + (4 * cm), y, reserva.itinerario.recorrido.nombre_recorrido[:30])  # Limitar a 30 chars
            p.drawString(x + (10 * cm), y, reserva.turista.get_full_name()[:25])  # Limitar a 25 chars
            p.drawString(x + (14 * cm), y, str(reserva.cantidad_asientos))

            y -= 0.7 * cm  # Bajar 0.7 cm para la siguiente fila

            # (Opcional: Control simple de salto de página)
            if y < (3 * cm):  # Si nos quedan menos de 3cm
                p.showPage()  # Cerrar página actual y crear una nueva
                p.setFont("Helvetica", 10)  # Resetear la fuente
                y = height - (2 * cm)  # Resetear Y

        # 8. Dibujar el Total
        y -= 0.5 * cm
        p.line(x, y, width - (2 * cm), y)  # Línea separadora
        y -= 0.5 * cm
        p.setFont("Helvetica-Bold", 12)
        p.drawString(x, y, f"Total de Pasajeros en el período: {total_pasajeros}")

        # 9. Cerrar y guardar el PDF
        p.showPage()
        p.save()
        return response


    elif formato == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="reporte_pasajeros_{fecha_inicio_str}_al_{fecha_fin_str}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Pasajeros por Fecha"
        header_font = Font(bold=True, name='Arial', size=12)
        center_align = Alignment(horizontal='center')
        ws['A1'] = "Reporte de Pasajeros por Fecha"
        ws['A1'].font = Font(bold=True, name='Arial', size=16)
        ws['A2'] = f"Período: {fecha_inicio_str} al {fecha_fin_str}"
        ws['A3'] = "Estado: CONFIRMADAS"
        headers = ['ID Reserva', 'Fecha Viaje', 'Recorrido', 'Turista', 'Asientos']
        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_num, value=header_title)
            cell.font = header_font
            ws.column_dimensions[chr(64 + col_num)].width = 25  # Ancho de columna
        row_num = 6

        for reserva in reservas:
            ws.append([
                reserva.id,
                reserva.itinerario.fecha_itinerario,
                reserva.itinerario.recorrido.nombre_recorrido,
                reserva.turista.get_full_name(),
                reserva.cantidad_asientos
            ])
            ws.cell(row=row_num, column=5).alignment = center_align
            row_num += 1

        total_row = row_num + 1
        ws.cell(row=total_row, column=4, value="Total de Pasajeros:").font = header_font
        ws.cell(row=total_row, column=5, value=total_pasajeros).font = header_font
        ws.cell(row=total_row, column=5).alignment = center_align
        wb.save(response)

        return response

    return redirect('dashboard_informes')