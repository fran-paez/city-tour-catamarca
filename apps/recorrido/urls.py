from django.urls import path
from . import views

urlpatterns = [
    # Recorridos
    path('recorridos/', views.lista_recorridos, name='lista_recorridos'),
    path('recorrido/crear/', views.crear_recorrido, name='crear_recorrido'),

    # Paradas
    path('paradas/', views.lista_paradas, name='lista_paradas'),
    path('parada/crear/', views.crear_parada, name='crear_parada'),

    # # Itinerarios
    path('itinerario/crear/', views.crear_itinerario, name='crear_itinerario'),
    path('itinerarios/', views.lista_itinerarios, name='lista_itinerarios'),

    # Unidades
    path('unidades/', views.lista_unidades, name='lista_unidades'),
    path('unidad/cargar/', views.agregar_unidad, name='agregar_unidad'),

    # Pagina principal
    path('', views.pagina_principal, name='pagina_principal'),
]
