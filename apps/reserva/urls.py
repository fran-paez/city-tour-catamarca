from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('paradas/', views.paradas_disponibles, name='paradas_disponibles'),
    path('parada/<int:parada_id>/', views.parada_detalles, name='parada_detalles'),

    # --- Panel de Notificaciones
    path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    path('notificaciones/crear/', views.crear_notificacion, name='crear_notificacion'),
    path('notificaciones/editar/<int:pk>/', views.editar_notificacion, name='editar_notificacion'),
    path('notificaciones/eliminar/<int:pk>/', views.eliminar_notificacion, name='eliminar_notificacion'),

    # --- Crud de reservas del turista ---
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('detalle/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
    path('cancelar/<int:pk>/', views.cancelar_reserva, name='cancelar_reserva'),
    # path('recorridos/', views.lista_reservas, name='recorridos_disponibles'),
]