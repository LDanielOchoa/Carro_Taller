"""
URL configuration for CarroTaller project.

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
from django.urls import include, path
from CarroTaller import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registros/insertar/', views.insertarRegistros, name='insertar'),
    path('registros/listado/', views.listadoRegistros, name='listado'),
    path('registros/listadoInactivos/', views.listadoRegistrosInactivos, name='listadoInactivos'),
    path('registros/actualizar/<int:id>', views.actualizarRegistro, name='actualizar'),
    path('registros/informacionRegistro/<int:id>/', views.informacionRegistro, name='informacionRegistro'),
    path('buscar/', views.buscarRegistros, name='buscar_registros'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.iniciarSesion, name='login'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('usuarios/crear/', views.crearVigilante, name='crear'),
    path('registros/detalleRegistro/<int:registro_id>/', views.guardarDetalles, name='detalle_registro'),
    path('registros/fotosDetalle/<int:detalle_carro_id>/', views.subirFotos, name='subir_fotos'),
    path('registros/ingresarHoraEntrada/<int:registro_id>/', views.ingresarHoraEntrada, name='ingresar_hora_entrada'),
    path('registros/listadoDetallesFotos/<int:registro_id>/', views.listadoDetallesYFotos, name='detalles_fotos'),
    path('registros/buscarOperador', views.buscarOperador, name='buscar_operador'),
    path('registros/buscarAcompanante', views.buscarAcompanante, name='buscar_acompanante'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
