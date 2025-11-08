from django.db import models
from django.core.validators import MinValueValidator
from apps.usuario.models import Usuario
from apps.recorrido.models import Itinerario, Parada
# Create your models here.

class Reserva(models.Model):
    """
    Representa la reserva de uno o más asientos en un Itinerario
    específico, hecha por un Turista.
    """
    # Definimos los 'choices' para el campo estado
    ESTADOS_RESERVA = [
        ('P', 'Pendiente'),
        ('C', 'Confirmada'),
        ('A', 'Cancelada'),
    ]

    # --- Atributos/Campos ---

    # ForeignKey a Usuario (el turista que reserva)
    turista = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,  # Si se borra el usuario, se borran sus reservas
        related_name='reservas'
    )

    # ForeignKey a Itinerario (el viaje específico que se reserva)
    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,  # Si se borra el itinerario, se borran sus reservas
        related_name='reservas'
    )

    # ForeignKey a Parada (dónde se sube el turista)
    punto_partida = models.ForeignKey(
        Parada,
        on_delete=models.SET_NULL,  # Si se borra la parada, la reserva no se borra
        null=True,
        related_name='reservas_origen'
    )

    cantidad_asientos = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Cantidad de asientos que reserva el turista"
    )

    fecha_reserva = models.DateTimeField(
        auto_now_add=True,  # Se establece automáticamente al crear la reserva
        help_text="Fecha y hora en que se realizó la reserva"
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADOS_RESERVA,
        default='P',  # Por defecto, una reserva nueva está 'Pendiente'
        help_text="Estado actual de la reserva (Pendiente, Confirmada, Cancelada)"
    )

    def __str__(self):
        return f"Reserva de {self.turista.username} para {self.itinerario}"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"


# === Modelo Notificacion ===
# Basado en tu CSV: "Mensajes a los turistas y en la página principal."

class Notificacion(models.Model):
    """
    Permite a los Operadores/Administradores emitir notificaciones
    generales o sobre un itinerario específico.
    """

    # --- Atributos/Campos ---

    titulo = models.CharField(max_length=200)

    mensaje = models.TextField()

    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación de la notificación"
    )

    es_publica = models.BooleanField(
        default=True,
        help_text="Si es True, se muestra en la página principal para todos"
    )

    # ForeignKey a Itinerario
    itinerario_afectado = models.ForeignKey(
        Itinerario,
        on_delete=models.SET_NULL,  # Si se borra el itinerario, la notificación no
        null=True,
        related_name='notificaciones'
    )

    # ForeignKey a Usuario (quién creó la notificación)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,  # Guardamos la notificación aunque se borre el admin
        null=True,
        related_name='notificaciones_creadas'
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_hora']  # Muestra las más nuevas primero