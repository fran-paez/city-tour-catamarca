from django.urls import path
from . import views

urlpatterns = [
    # Recorridos
    path('recorridos/', views.lista_recorridos, name='lista_recorridos'),
    path('recorrido/crear/', views.crear_recorrido, name='crear_recorrido'),
    path('recorrido/editar/<int:pk>/', views.editar_recorrido, name='editar_recorrido'),
    path('recorrido/eliminar/<int:pk>/', views.eliminar_recorrido, name='eliminar_recorrido'),

    # Paradas
    path('paradas/', views.lista_paradas, name='lista_paradas'),
    path('parada/crear/', views.crear_parada, name='crear_parada'),
    path('parada/editar/<int:pk>/', views.editar_parada, name='editar_parada'),
    path('parada/eliminar/<int:pk>/', views.eliminar_parada, name='eliminar_parada'),

    # # Itinerarios
    path('itinerario/crear/', views.crear_itinerario, name='crear_itinerario'),
    path('itinerarios/', views.lista_itinerarios, name='lista_itinerarios'),
    path('itinerario/editar/<int:pk>/', views.editar_itinerario, name='editar_itinerario'),
    path('itinerario/eliminar/<int:pk>/', views.eliminar_itinerario, name='eliminar_itinerario'),

    # Unidades
    path('unidades/', views.lista_unidades, name='lista_unidades'),
    path('unidad/cargar/', views.agregar_unidad, name='agregar_unidad'),
    path('unidad/editar/<int:pk>/', views.editar_unidad, name='editar_unidad'),
    path('unidad/eliminar/<int:pk>/', views.eliminar_unidad, name='eliminar_unidad'),
]