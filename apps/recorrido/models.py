from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import os
from django.utils.text import slugify
from django.conf import settings
# Para señales
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings



def renombrar_imagen_parada(instance, filename):
    extension = os.path.splitext(filename)[1]
    if instance.id:
        # Si ya tiene ID, usarlo
        nuevo_nombre = f"parada_{instance.id}{extension}"
    else:
        # Si no tiene id es pq es nuevo, usar nombre temporal
        # Se renombrará correctamente después de que se guarde en la bd
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

    imagen = models.ImageField(upload_to=renombrar_imagen_parada, blank=True, null=True,
    default='paradas/default.jpg')


    def __str__(self):
        return f"Parada {self.id} - {self.descripcion_parada[:30]}"







class Recorrido(models.Model):
    descripcion = models.TextField()
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
        return f"Recorrido {self.id} - {self.descripcion[:40]}"
    

class Itinerario(models.Model):
    recorrido = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='itinerarios')
    unidad = models.ForeignKey('Unidad', on_delete=models.PROTECT, related_name='itinerarios')
    fecha_itinerario = models.DateField()
    hora_itinerario = models.TimeField()
    # Los cupos se inicializan al crear la instancia desde la cantidad de asientos de la unidad
    cupos = models.IntegerField()

    def clean(self):
        # Validaciones a
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
        # Si es creación (no tiene pk aún) y existe unidad pero no se proporcionaron cupos,
        # inicializamos cupos con la cantidad de asientos de la unidad.
        if self.pk is None:
            # intentar inicializar cupos si no se pasó o es falsy (0)
            try:
                if (self.cupos is None or self.cupos == 0) and getattr(self, 'unidad', None):
                    self.cupos = self.unidad.cantidad_asientos
            except Exception:
                # unidad posiblemente no resuelta aún; dejaremos que clean/migrate gestione errores
                pass

        # Validar para recien guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Itinerario {self.id} - {self.recorrido.descripcion[:30]} ({self.fecha_itinerario} {self.hora_itinerario})"


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
    


    # -----------------------------SEÑALES-----------------------------
    # Esta señal renombra la imagen de la parada después de guardarla por primera vez
    # Esta función se implementa ya que si para ponerle el nombre del ID de la imagen es
    # necesario que primero lo guarde en la base de datos, si no le pone de nombre parada_None
    # al no poder saber el id que le toca.
    @receiver(post_save, sender=Parada)
    def renombrar_imagen_actual(sender, instance, **kwargs):
        if instance.imagen and instance.imagen.name != 'paradas/default.jpg':
            # Verificar si la imagen tiene el nombre temporal con "None"
            if 'temp_' in instance.imagen.name:
                # Obtener extensión del archivo actual
                extension = os.path.splitext(instance.imagen.name)[1]
                nuevo_nombre = f"paradas/parada_{instance.id}{extension}"
                
                # Renombrar el archivo físico
                vieja_ruta = instance.imagen.path
                nueva_ruta = os.path.join(settings.MEDIA_ROOT, nuevo_nombre)
                
                # Asegurarse de que el directorio existe
                os.makedirs(os.path.dirname(nueva_ruta), exist_ok=True)
                
                # Renombrar el archivo
                if os.path.exists(vieja_ruta):
                    os.rename(vieja_ruta, nueva_ruta)
                    instance.imagen.name = nuevo_nombre
                    # Guardar sin triggering la señal de nuevo
                    sender.objects.filter(pk=instance.pk).update(imagen=nuevo_nombre)