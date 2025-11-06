# apps/usuario/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Rol, Usuario

class RolForm(forms.ModelForm):
    """
    Formulario de Django basado en el modelo Rol.
    """
    class Meta:
        model = Rol
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'descripcion']


# --- NUEVO FORMULARIO PARA USUARIOS ---

class UsuarioCreationForm(UserCreationForm):
    """
    Un formulario personalizado para crear usuarios.
    Hereda de UserCreationForm para manejar el hasheo de contraseñas.
    """


    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        required=True,
        label="Rol del usuario"
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'rol')

    def save(self, commit=True):
        # Sobrescribimos el metodo save()
        user = super().save(commit=False)

        user.rol = self.cleaned_data['rol']

        if commit:
            user.save()
        return user