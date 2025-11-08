from django.urls import path
from . import views

urlpatterns = [
    # Ejemplo temporal para evitar errores
    path('', views.index, name='informe_index'),
]
