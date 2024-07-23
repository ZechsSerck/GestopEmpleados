from django.contrib import admin
from .models import *
# Register your models here.


# conexion a la tabla
admin.site.register(Empleado)
admin.site.register(Cargo)
admin.site.register(Departamento)
admin.site.register(Area)
admin.site.register(ContactoEmergencia)
admin.site.register(CargaFamiliar)
