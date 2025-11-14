# apps/informe/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. El dashboard que muestra los formularios
    path('', views.dashboard_informes, name='dashboard_informes'),

    # 2. URL para consulta por fecha
    path('pasajeros_por_fecha/', views.generar_informe_pasajeros_fechas, name='informe_pasajeros_fechas'),

    # 3. URL para consulta de reservas de un recorrido específico
    path('reservas_por_recorrido/', views.generar_informe_por_recorrido, name='informe_reservas_por_recorrido'),

    # 4. URL para el informe de Recorridos Activos
    path('recorridos_activos/', views.generar_informe_recorridos_activos, name='informe_recorridos_activos'),

    # 5. URL para el informe de Paradas más Utilizadas
    path('paradas_utilizadas/', views.generar_informe_paradas_utilizadas, name='informe_paradas_utilizadas'),
]