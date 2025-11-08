from django import forms
from .models import Parada, Recorrido, Itinerario, Unidad

class ParadaForm(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['nombre', 'descripcion_parada', 'imagen', 'estado', 'visibilidad_pagina']
        widgets = {
            'descripcion_parada': forms.Textarea(attrs={'rows': 2, 'cols': 35}),
        }

class RecorridoForm(forms.ModelForm):
    class Meta:
        model = Recorrido
        fields = ['descripcion', 'paradas', 'duracion', 'precio', 'estado']
        widgets = {
            'paradas': forms.CheckboxSelectMultiple(),
        }

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['patente', 'cantidad_asientos', 'estado']


# VERFICAR
class ItinerarioForm(forms.ModelForm):
    class Meta:
        model = Itinerario
        fields = ['recorrido', 'unidad', 'fecha_itinerario', 'hora_itinerario']
        widgets = {
            'fecha_itinerario': forms.DateInput(attrs={'type': 'date'}),
            'hora_itinerario': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        unidad = cleaned_data.get('unidad')
        
        if unidad:
            # Inicializar cupos con la cantidad de asientos de la unidad
            cleaned_data['cupos'] = unidad.cantidad_asientos
        
        return cleaned_data