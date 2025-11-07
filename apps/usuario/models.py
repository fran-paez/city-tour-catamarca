from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Rol(models.Model):
    """
    Define los tipos de roles de usuario en el sistema (Administrador, Turista, Operador).
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    # sobreescribir save para guardar el nombre de los roles siempre con mayusculas
    def save(self, *args, **kwargs):
        # Convierte el nombre a mayúsculas ANTES de guardarlo
        self.nombre = self.nombre.upper()
        # Llama al metodo save() original para que lo guarde en la BD
        super(Rol, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class Usuario(AbstractUser):
    """
    Modelo de usuario extendido para incluir el rol del sistema.
    """
    # relacion 1:M con Rol
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,  # Mantiene el usuario si se elimina el rol (queda null)
        null=True,
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rol.nombre if self.rol else 'Sin Rol'})"
