from django.urls import path
from . import views

urlpatterns = [
    path('parada/crear/', views.crear_parada, name='crear_parada'),
    # path('paradas/', views.lista_paradas, name='lista_paradas')  # opcional
]
urlpatterns = [
    path('parada/crear/', views.crear_parada, name='crear_parada'),
    path('paradas/', views.lista_paradas, name='lista_paradas'),
]
