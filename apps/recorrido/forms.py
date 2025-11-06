from django import forms
from .models import Parada, Recorrido

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['nombre', 'descripcion_parada', 'estado', 'visibilidad_pagina']
        widgets = {
            'descripcion_parada': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class RecorridoForm(forms.ModelForm):
    class Meta:
        model = Recorrido
        fields = ['descripcion', 'paradas', 'duracion', 'precio', 'estado']
        widgets = {
            'paradas': forms.CheckboxSelectMultiple(),
        }