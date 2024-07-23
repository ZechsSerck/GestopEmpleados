from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from .models import Empleado, ContactoEmergencia, CargaFamiliar


class empleadoForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all(),
                            required=True, label="Usuario")

    class Meta:
        model = Empleado
        fields = ['RUT', 'nombre', 'apellido1', 'apellido2', 'sexo', 'direccion',
                  'telefono', 'cargo_id', 'departamento_id', 'area_id', 'user']


class contactoForm(ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['RUT_contacto', 'RUT', 'nombre', 'apellido1_contacto',
                  'apellido2_contacto', 'relacion', 'telefono']


class cargaForm(ModelForm):
    class Meta:
        model = CargaFamiliar
        fields = ['RUT_carga', 'RUT', 'nombre_carga',
                  'apellido1_carga', 'apellido2_carga', 'parentesco', 'sexo']
