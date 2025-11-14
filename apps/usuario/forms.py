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
    - Si no hay ningún admin, asigna 'ADMINISTRADOR' al primer usuario creado.
    - Si ya existe un admin, asigna 'TURISTA' por defecto.
    """

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)

        try:
            # Verificar si ya existe un administrador en el sistema
            if Usuario.objects.filter(rol__nombre='ADMINISTRADOR').exists():
                # Si ya hay un admin, el nuevo usuario será Turista
                rol_a_asignar, _ = Rol.objects.get_or_create(nombre="TURISTA")
            else:
                # Si no hay ningún admin, este nuevo usuario será el primero
                rol_a_asignar, _ = Rol.objects.get_or_create(nombre="ADMINISTRADOR")
            
            user.rol = rol_a_asignar

        except Exception as e:
            # Imprimir un error en la consola del servidor si algo falla
            print(f"Error al asignar rol durante la creación de usuario: {e}")

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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UsuarioChangeForm, self).__init__(*args, **kwargs)

        if self.instance and self.request:
            es_admin = self.request.user.rol.nombre == 'ADMINISTRADOR'
            es_el_mismo_usuario = self.request.user.id == self.instance.id

            if es_admin and es_el_mismo_usuario:
                self.fields['rol'].disabled = True
                self.fields['is_active'].disabled = True

    def save(self, commit=True):
        user = super(UsuarioChangeForm, self).save(commit=False)

        if self.request:
            es_admin = self.request.user.rol.nombre == 'ADMINISTRADOR'
            es_el_mismo_usuario = self.request.user.id == self.instance.id

            if es_admin and es_el_mismo_usuario:
                user.rol = self.request.user.rol
                user.is_active = True

        if commit:
            user.save()
        return user

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'rol', 'is_active')