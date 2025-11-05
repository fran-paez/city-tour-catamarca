from django import forms
from .models import Parada

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['latitud', 'longitud', 'descripcion', 'estado', 'visibilidad_pagina']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
