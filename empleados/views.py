from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.db.models import Count, Sum
from .models import Empleado
from .forms import *

# Create your views here.


def inicio(request):
    return render(request, 'miPerfil')


def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm()
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    login(request, user)
                    return redirect('inicioSesion')
                else:
                    return render(request, 'registro.html', {
                        'form': form,
                        'error': 'El usuario ya existe'
                    })
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'registro.html', {
                'form': UserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })


def inicioSesion(request):
    if request.method == 'GET':
        return render(request, 'inicioSesion.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inicioSesion.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('lista')
            else:
                return redirect('miPerfil')


@login_required
def agregarUsuario(request):
    if request.method == 'GET':
        form = empleadoForm()
        return render(request, 'agregarUsuario.html', {'form': form})
    else:
        try:
            form = empleadoForm(request.POST)
            if form.is_valid():
                new_empleado = form.save(commit=False)
                new_empleado.user = form.cleaned_data['user']
                new_empleado.save()
                # Cambiado a 'lista' para redirigir después de agregar el usuario
                return redirect('lista')
            else:
                return render(request, 'agregarUsuario.html', {'form': form, 'error': 'Datos inválidos'})
        except ValueError:
            return render(request, 'agregarUsuario.html', {'form': empleadoForm(), 'error': 'Datos inválidos'})


@login_required
def agregarCarga(request):
    try:
        empleado = Empleado.objects.get(user=request.user)
    except Empleado.DoesNotExist:
        empleado = None

    if request.method == 'GET':
        return render(request, 'agregarCarga.html', {
            'form': cargaForm,
            'empleado': empleado
        })
    else:
        try:
            form = cargaForm(request.POST)
            if form.is_valid():
                new_carga = form.save(commit=False)
                # Asocia la carga familiar con el empleado del usuario
                new_carga.RUT = Empleado.objects.get(user=request.user)
                new_carga.save()
                return redirect('miPerfil')
        except ValueError:
            return render(request, 'agregarCarga.html', {
                'form': cargaForm,
                'empleado': empleado,
                'error': 'Datos Invalidos'
            })


@login_required
def agregarContacto(request):
    try:
        empleado = Empleado.objects.get(user=request.user)
    except Empleado.DoesNotExist:
        empleado = None

    if request.method == 'GET':
        return render(request, 'agregarContacto.html', {
            'form': contactoForm,
            'empleado': empleado
        })
    else:
        try:
            form = contactoForm(request.POST)
            if form.is_valid():
                new_contacto = form.save(commit=False)
                new_contacto.RUT = Empleado.objects.get(user=request.user)
                new_contacto.save()
                return redirect('miPerfil')
        except ValueError:
            return render(request, 'agregarContacto.html', {
                'form': contactoForm,
                'empleado': empleado,
                'error': 'Datos Invalidos'
            })


@login_required
def lista(request):
    if request.user.is_superuser:
        empleados = list(Empleado.objects.select_related(
            'cargo_id', 'area_id').all())
        usuarios_sin_empleado = list(
            User.objects.filter(empleado__isnull=True))
        items = [{'RUT': empleado.RUT, 'nombre': empleado.nombre, 'apellido1': empleado.apellido1, 'apellido2': empleado.apellido2,
                  'sexo': empleado.sexo, 'area': empleado.area_id.nombre_sucursal, 'cargo': empleado.cargo_id.nombre_cargo,
                  'tipo': 'empleado'} for empleado in empleados] + \
            [{'RUT': usuario.username, 'nombre': usuario.username, 'apellido1': '', 'apellido2': '',
              'sexo': '', 'area': '', 'cargo': '', 'tipo': 'usuario'} for usuario in usuarios_sin_empleado]
    else:
        items = []
    return render(request, 'lista.html', {'items': items})


@login_required
def miPerfil(request):
    try:
        empleado = Empleado.objects.select_related(
            'cargo_id', 'area_id').get(user=request.user)
        cargas = CargaFamiliar.objects.filter(RUT=empleado)
        contactos = ContactoEmergencia.objects.filter(RUT=empleado)
    except Empleado.DoesNotExist:
        empleado = None
        cargas = []
        contactos = []
    return render(request, 'miPerfil.html', {'empleado': empleado, 'cargas': cargas,
                                             'contactos': contactos})


@login_required
def estadisticas(request):
    if request.user.is_superuser:
        # Contar empleados por área
        empleados_por_area = Empleado.objects.values('area_id__nombre_sucursal').annotate(
            total_empleados=Count('RUT')).order_by('area_id__nombre_sucursal')

        # Calcular el salario total por departamento
        salario_por_departamento = Empleado.objects.values('departamento_id__nombre_departamento').annotate(
            total_salario=Sum('cargo_id__salario')).order_by('departamento_id__nombre_departamento')

        # Contar empleados por cargo
        empleados_por_cargo = Empleado.objects.values('cargo_id__nombre_cargo').annotate(
            total_empleados=Count('RUT')).order_by('cargo_id__nombre_cargo')

        # Obtener el salario promedio por cargo
        salario_promedio_por_cargo = Empleado.objects.values('cargo_id__nombre_cargo').annotate(
            salario_promedio=Sum('cargo_id__salario') / Count('RUT')).order_by('cargo_id__nombre_cargo')

        context = {
            'empleados_por_area': empleados_por_area,
            'salario_por_departamento': salario_por_departamento,
            'empleados_por_cargo': empleados_por_cargo,
            'salario_promedio_por_cargo': salario_promedio_por_cargo,
        }

        return render(request, 'estadisticas.html', context)
    else:
        return redirect('miPerfil')


@login_required
def actualizarContacto(request, contacto_id):
    try:
        contacto = ContactoEmergencia.objects.get(
            pk=contacto_id, RUT__user=request.user)
        if request.method == 'GET':
            form = contactoForm(instance=contacto)
            return render(request, 'actualizarContacto.html', {'form': form, 'contacto': contacto})
        else:
            form = contactoForm(request.POST, instance=contacto)
            if form.is_valid():
                form.save()
                return redirect('miPerfil')
            else:
                return render(request, 'actualizarContacto.html', {'form': form,
                                                                   'error': 'Datos Inválidos',
                                                                   'contacto': contacto})
    except ContactoEmergencia.DoesNotExist:
        return redirect('miPerfil')


@login_required
def detalleEmpleado(request, rut):
    empleado = get_object_or_404(Empleado, pk=rut)
    if request.method == 'GET':
        form = empleadoForm(instance=empleado)
        return render(request, 'detalleEmpleado.html', {'empleado': empleado, 'form': form,
                                                        'is_superuser': request.user.is_superuser})
    else:
        if request.user.is_superuser:
            try:
                form = empleadoForm(request.POST, instance=empleado)
                if form.is_valid():
                    form.save()
                    return redirect('lista')
                return render(request, 'detalleEmpleado.html', {'empleado': empleado, 'form': form,
                                                                'is_superuser': True})
            except ValueError:
                return render(request, 'detalleEmpleado.html', {'empleado': empleado, 'form': form,
                                                                'is_superuser': True, 'error': "Error al actualizar"})
        else:
            return render(request, 'detalleEmpleado.html', {'empleado': empleado, 'form': form,
                                                            'is_superuser': False, 'error': "No tienes permiso para modificar este formulario"})


@login_required
def editarUsuario(request):
    return render(request, 'editarUsuario.html')


@login_required
def borrarEmpleado(request, rut):
    if not request.user.is_superuser:
        return render(request, 'error.html', {'error': 'No tienes permiso para realizar esta acción.'})

    empleado = get_object_or_404(Empleado, pk=rut)

    if request.method == 'POST':
        empleado.delete()
        return redirect('lista')

    return render(request, 'confirmar_borrar.html', {'empleado': empleado})


def signout(request):
    logout(request)
    return redirect('inicioSesion')


def variables(request):
    return render(request, 'variables.html')


def home(request):
    return render(request, 'home.html')


def aviso(request):
    return render(request, 'aviso.html')
