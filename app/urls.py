from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('registrar/', registrar, name="registrar"),
    path('perfil/', perfil, name="perfil"),
    path('historial_productos/', historial_productos, name="historial_productos"),
    path('historial_servicios/', historial_servicios, name="historial_servicios"),
    path('empresas_servicios/', empresas_servicios, name="empresas_servicios"),
    path('detalles_servicios/', detalles_servicios, name="detalles_servicios"),
    path('productos/', productos, name="productos"),
    path('carrito/', carrito, name="carrito"),
    path('solicitud_servicio/', solicitud_servicio, name="solicitud_servicio"),
    path('despacho/', despacho, name="despacho"),
]