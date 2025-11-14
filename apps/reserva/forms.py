from django import forms
from django.utils import timezone
from .models import Notificacion, Reserva
from apps.recorrido.models import Itinerario, Parada

# FORMULARIO PARA NOTIFICACIONES
class NotificacionForm(forms.ModelForm):
    """
    Formulario para crear y editar Notificaciones.
    """
    # itinerario opcional, asi la notificación puede ser general
    itinerario_afectado = forms.ModelChoiceField(
        queryset=Itinerario.objects.all().order_by('-fecha_itinerario'),
        required=False,
        label="Itinerario Afectado (Opcional)"
    )

    class Meta:
        model = Notificacion
        # El campo 'creado_por' se asignará automáticamente en la vista
        fields = ['titulo', 'mensaje', 'es_publica', 'itinerario_afectado']
        labels = {
            'es_publica': '¿Mostrar en la Página Principal?',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'es_publica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# FORMULARIO PARA RESERVAS
class ReservaForm(forms.ModelForm):
    """
    Formulario para que el Turista cree una nueva reserva.
    """
    # mostrar solo los viajes que aún no han pasado.
    itinerario = forms.ModelChoiceField(
        queryset=Itinerario.objects.filter(
            fecha_itinerario__gte=timezone.now().date()  # Solo de hoy en adelante
        ).order_by('fecha_itinerario', 'hora_itinerario'),
        label="Selecciona tu viaje (Fecha y Hora)"
    )

    # Filtramos las paradas para mostrar solo las activas
    punto_partida = forms.ModelChoiceField(
        queryset=Parada.objects.filter(estado='activo'),
        label="Selecciona tu Punto de Partida"
    )

    class Meta:
        model = Reserva
        # El turista solo debe elegir estas 3 cosas.
        # 'turista' y 'estado' se asignan en la vista.
        fields = ['itinerario', 'punto_partida', 'cantidad_asientos']
        labels = {
            'cantidad_asientos': 'Cantidad de Asientos',
        }

    def __init__(self, *args, **kwargs):
        """
        Permite pre-seleccionar un itinerario si se pasa
        un 'itinerario_id' al crear el formulario.
        """
        itinerario_inicial = kwargs.pop('itinerario_id', None)
        super().__init__(*args, **kwargs)

        if itinerario_inicial:
            self.fields['itinerario'].initial = itinerario_inicial

    def clean(self):
        """
        Validación personalizada para verificar los cupos.
        """
        cleaned_data = super().clean()
        itinerario = cleaned_data.get('itinerario')
        cantidad = cleaned_data.get('cantidad_asientos')

        if itinerario and cantidad:
            if itinerario.cupos < cantidad:
                # Si no hay cupos, lanzamos un error de validación
                raise forms.ValidationError(
                    f"No hay suficientes cupos. Disponibles: {itinerario.cupos}"
                )
        return cleaned_data