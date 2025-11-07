# apps/usuario/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Rol, Usuario

class RolForm(forms.ModelForm):
    """
    Formulario de Django basado en el modelo Rol.
    """
    class Meta:
        model = Rol
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'descripcion']


# --- FORMULARIO PARA USUARIOS ---

class UsuarioCreationForm(UserCreationForm):
    """
    Formulario para el registro de usuarios (crear Usuario).
    Asigna 'Turista' por defecto.
    """

    # PASO 1: Hemos ELIMINADO el campo 'rol = forms.ModelChoiceField(...)'
    # que estaba aquí. Ya no es necesario.

    class Meta(UserCreationForm.Meta):
        model = Usuario

        # PASO 2: Hemos ELIMINADO 'rol' de esta lista de campos.
        # Ahora el formulario solo pedirá estos datos.
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        # PASO 3: Sobrescribimos el metodo save() para asignar el rol.

        # Primero, corremos el save() original (sin guardar en BD)
        # Esto nos da el objeto 'user' con la contraseña ya hasheada.
        user = super().save(commit=False)

        try:
            # --- MODIFICACIÓN AQUÍ ---
            # Ahora buscamos o creamos el rol "TURISTA" en mayúsculas
            turista_rol, created = Rol.objects.get_or_create(nombre="TURISTA")

            user.rol = turista_rol

        except Exception as e:
            print(f"Error al asignar rol 'TURISTA' por defecto: {e}")

        if commit:
            user.save()
        return user

# --- FORMULARIO EDICION USUARIO ---

class UsuarioChangeForm(UserChangeForm):
    """
    Formulario para actualizar un usuario existente.
    Usado por Administradores (o usuarios para su propio perfil).
    """
    password = None

    # Añadimos el campo rol para que el Admin pueda editarlo
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        required=True,
        label="Rol del usuario"
    )

    class Meta:
        model = Usuario
        # Campos que se podrán editar
        fields = ('username', 'first_name', 'last_name', 'email', 'rol', 'is_active')