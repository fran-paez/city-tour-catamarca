from django import forms
from .models import Parada

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['nombre', 'descripcion_parada', 'estado', 'visibilidad_pagina']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
