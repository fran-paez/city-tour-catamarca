from django import forms
from .models import Notificacion
from apps.recorrido.models import Itinerario


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