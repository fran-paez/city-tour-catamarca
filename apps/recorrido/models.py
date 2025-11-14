from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import os
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

def renombrar_imagen_parada(instance, filename):
    extension = os.path.splitext(filename)[1]
    if instance.id:
        nuevo_nombre = f"parada_{instance.id}{extension}"
    else:
        nombre_temporal = f"temp_{slugify(instance.nombre)}{extension}"
        return os.path.join('paradas/temp/', nombre_temporal)
    return os.path.join('paradas/', nuevo_nombre)

class Parada(models.Model):
    nombre = models.CharField(max_length=60)
    descripcion_parada = models.TextField()
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')
    visibilidad_pagina = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to=renombrar_imagen_parada, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = 'paradas/default.png'
        super().save(*args, **kwargs)

    @property
    def imagen_url(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        # Fallback por si la imagen no se encuentra o hay un error
        return os.path.join(settings.STATIC_URL, 'recorrido/img/default.png')

    def __str__(self):
        return f"Parada {self.id} - {self.nombre[:30]}"

class Recorrido(models.Model):
    nombre_recorrido=  models.CharField(max_length=30)
    descripcion_recorrido = models.TextField()
    paradas = models.ManyToManyField(
        Parada,
        related_name='recorridos'
    )
    duracion = models.IntegerField(help_text="MIN")
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Recorrido {self.id} - {self.descripcion_recorrido[:40]}"

class Itinerario(models.Model):
    recorrido = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='itinerarios')
    unidad = models.ForeignKey('Unidad', on_delete=models.PROTECT, related_name='itinerarios')
    fecha_itinerario = models.DateField()
    hora_itinerario = models.TimeField()
    cupos = models.IntegerField()

    def clean(self):
        errors = {}
        if not self.recorrido_id:
            errors['recorrido'] = 'Debe tener un recorrido asociado.'
        if not self.unidad_id:
            errors['unidad'] = 'Debe tener una unidad asociada.'
        if not self.fecha_itinerario:
            errors['fecha_itinerario'] = 'Debe tener una fecha.'
        if not self.hora_itinerario:
            errors['hora_itinerario'] = 'Debe tener una hora.'
        if self.unidad_id and self.cupos is not None:
            max_asientos = self.unidad.cantidad_asientos
            if self.cupos < 0:
                errors['cupos'] = 'Los cupos no pueden ser negativos.'
            elif self.cupos > max_asientos:
                errors['cupos'] = f'Los cupos no pueden superar la cantidad de asientos de la unidad ({max_asientos}).'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.pk is None:
            try:
                if (self.cupos is None or self.cupos == 0) and getattr(self, 'unidad', None):
                    self.cupos = self.unidad.cantidad_asientos
            except Exception:
                pass
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Itinerario {self.id} - {self.recorrido.descripcion_recorrido[:30]} ({self.fecha_itinerario} {self.hora_itinerario})"

class Unidad(models.Model):
    patente = models.CharField(max_length=7, unique=True)
    cantidad_asientos = models.IntegerField(validators=[MinValueValidator(10)])
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"Unidad {self.id} - {self.patente} ({self.cantidad_asientos} asientos)"

@receiver(post_save, sender=Parada)
def renombrar_imagen_actual(sender, instance, **kwargs):
    if instance.imagen and 'temp_' in instance.imagen.name:
        extension = os.path.splitext(instance.imagen.name)[1]
        nuevo_nombre = f"paradas/parada_{instance.id}{extension}"
        vieja_ruta = instance.imagen.path
        nueva_ruta = os.path.join(settings.MEDIA_ROOT, nuevo_nombre)
        os.makedirs(os.path.dirname(nueva_ruta), exist_ok=True)
        if os.path.exists(vieja_ruta):
            os.rename(vieja_ruta, nueva_ruta)
            instance.imagen.name = nuevo_nombre
            Parada.objects.filter(pk=instance.pk).update(imagen=nuevo_nombre)