from django.db import models
from django.forms import ValidationError


class Parada(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion_parada = models.TextField()

    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')
    visibilidad_pagina = models.BooleanField(default=True)

    def __str__(self):
        return f"Parada {self.id} - {self.descripcion_parada[:30]}"

# --- MODELO RECORRIDO ---
class Recorrido(models.Model):
    descripcion = models.TextField()
    paradas = models.ManyToManyField(
        Parada,
        related_name='recorridos'
    )
    duracion = models.IntegerField(help_text="DuraciÃ³n del recorrido en minutos")
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Recorrido {self.id} - {self.descripcion[:40]}"
# --- MODELO ITINERARIO ---
class Itinerario(models.Model):
    recorrido = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='itinerarios')
    fecha_itinerario = models.DateField()
    hora_itinerario = models.TimeField()
    cupos = models.IntegerField()

    def __str__(self):
        return f"Itinerario {self.id} - {self.recorrido.descripcion[:30]} ({self.fecha_itinerario} {self.hora_itinerario})"