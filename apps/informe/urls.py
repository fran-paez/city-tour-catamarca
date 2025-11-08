# apps/informe/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. El dashboard que muestra los formularios
    path('', views.dashboard_informes, name='dashboard_informes'),

    # 2. Vista para consulta por fecha
    path('pasajeros_por_fecha/', views.generar_informe_pasajeros_fechas, name='informe_pasajeros_fechas'),
]