from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_sucursal = models.CharField(max_length=25)
    ciudad = models.CharField(max_length=25, null=True, blank=True)
    direccion_sucursal = models.CharField(max_length=45, null=True, blank=True)
    telefono_sucursal = models.CharField(max_length=15)

    def __str__(self):
        return self.ciudad + ' - ' + self.nombre_sucursal


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    encargado_departamento = models.CharField(
        max_length=40, null=True, blank=True)
    nombre_departamento = models.CharField(max_length=25)
    id_area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.encargado_departamento + ' - ' + self.nombre_departamento


class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=25)
    salario = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_cargo + ' - '


class Empleado(models.Model):
    RUT = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    sexo = models.CharField(max_length=9, null=True, blank=True)
    direccion = models.CharField(max_length=45, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo_id = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departamento_id = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.RUT + ' - ' + self.nombre + ' ' + self.apellido1


class ContactoEmergencia(models.Model):
    RUT_contacto = models.CharField(max_length=12, primary_key=True)
    RUT = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido1_contacto = models.CharField(max_length=20)
    apellido2_contacto = models.CharField(max_length=20, null=True, blank=True)
    relacion = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.RUT_contacto + ' - ' + self.nombre


class CargaFamiliar(models.Model):
    RUT_carga = models.CharField(max_length=12, primary_key=True)
    RUT = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nombre_carga = models.CharField(max_length=20)
    apellido1_carga = models.CharField(max_length=20)
    apellido2_carga = models.CharField(max_length=20, null=True, blank=True)
    parentesco = models.CharField(max_length=15, null=True, blank=True)
    sexo = models.CharField(max_length=9, null=True, blank=True)

    def __str__(self):
        return self.RUT_carga + ' - ' + self.nombre_carga
