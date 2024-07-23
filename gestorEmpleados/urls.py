"""
URL configuration for gestorEmpleados project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from empleados import views


urlpatterns = [
    path('', views.inicioSesion),
    path('admin/', admin.site.urls),
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.signout, name='logout'),
    path('inicioSesion/', views.inicioSesion, name='inicioSesion'),
    path('lista/', views.lista, name='lista'),
    path('lista/<str:rut>/', views.detalleEmpleado, name='detalleEmpleado'),
    path('lista/<str:rut>/borrar/', views.borrarEmpleado, name='borrarEmpleado'),
    path('miPerfil/', views.miPerfil, name='miPerfil'),
    path('editarUsuario/', views.editarUsuario, name='editarUsuario'),
    path('agregarUsuario/', views.agregarUsuario, name='agregarUsuario'),
    path('agregarCarga/', views.agregarCarga, name='agregarCarga'),
    path('agregarContacto/', views.agregarContacto, name='agregarContacto'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('actualizarContacto/<int:contacto_id>/',
         views.actualizarContacto, name='actualizarContacto'),
    path('variables/', views.variables, name='variables'),
    path('aviso/', views.aviso, name='aviso')
]
