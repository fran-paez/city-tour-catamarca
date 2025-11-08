from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('paradas/', views.paradas_disponibles, name='paradas_disponibles'),
    path('parada/<int:parada_id>/', views.parada_detalles, name='parada_detalles'),

    # path('recorridos/', views.lista_reservas, name='recorridos_disponibles'),
]