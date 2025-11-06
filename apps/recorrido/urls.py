from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    # Recorridos
    path('', views.lista_recorridos, name='lista_recorridos'),
    path('crear/', views.crear_recorrido, name='crear_recorrido'),
    # Paradas
    path('parada/crear', views.crear_parada, name='crear_parada'),
    path('paradas/', views.lista_paradas, name='lista_paradas'),
]
