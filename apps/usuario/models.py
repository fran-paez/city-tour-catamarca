from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# lado "UNO" de la relacion (roles)
class Rol(models.Model):
    """
    Define los tipos de roles de usuario en el sistema (Administrador, Turista, Operador).
    """
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


# lado "MUCHOS" de la relacion (usuarios)
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
