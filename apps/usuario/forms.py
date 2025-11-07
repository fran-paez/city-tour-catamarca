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

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        # Primero, corremos el save() original (sin guardar en BD)
        # Esto nos da el objeto 'user' con la contraseña ya hasheada.
        user = super().save(commit=False)

        try:
            # Ahora buscamos o creamos el rol "TURISTA"
            turista_rol, created = Rol.objects.get_or_create(nombre="TURISTA")
            user.rol = turista_rol

        except Exception as e:
            print(f"Error al asignar rol 'TURISTA' por defecto: {e}")

        if commit:
            user.save()
        return user

# --- FORMULARIO EDICION USUARIO ---

class UsuarioChangeForm(UserChangeForm):
    password = None
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        required=True,
        label="Rol del usuario"
    )

    # modificar constructor para que admin no pueda cambiar su propio rol
    def __init__(self, *args, **kwargs):
        # Capturamos el 'request' que pasamos desde la vista
        self.request = kwargs.pop('request', None)
        super(UsuarioChangeForm, self).__init__(*args, **kwargs)

        if self.instance and self.request:
            es_admin = self.request.user.rol.nombre == 'ADMINISTRADOR'
            es_el_mismo_usuario = self.request.user.id == self.instance.id

            # Si el Admin se está editando a sí mismo...
            if es_admin and es_el_mismo_usuario:
                #  deshabilitamos el campo 'rol'.
                self.fields['rol'].disabled = True

    # metodo save (PARA DOBLE SEGURIDAD) ---
    def save(self, commit=True):
        # Obtenemos el usuario antes de guardarlo
        user = super(UsuarioChangeForm, self).save(commit=False)

        # Verificamos la misma condición de seguridad
        if self.request:
            es_admin = self.request.user.rol.nombre == 'ADMINISTRADOR'
            es_el_mismo_usuario = self.request.user.id == self.instance.id

            if es_admin and es_el_mismo_usuario:
                # Si el Admin se está editando a sí mismo,
                # forzamos a que su rol sea el que ya tenía
                user.rol = self.request.user.rol

        if commit:
            user.save()
        return user

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'rol', 'is_active')