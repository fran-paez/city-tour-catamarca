# apps/usuario/forms.py

from django import forms
from .models import Rol

class RolForm(forms.ModelForm):
    """
    Formulario de Django basado en el modelo Rol.
    """
    class Meta:
        model = Rol
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'descripcion']