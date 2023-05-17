from django.urls import path
from.views import *

urlpatterns = [
path('',index, name="index"),
path('registrar/',registrar, name="registrar"),
path('productos/',productos,name="productos"),
path('historial/',historial, name="historial"),
path('solicitud_servicio/',solicitud_servicio, name="solicitud_servicio"),
path('despacho/',despacho,name="despacho"),
path('carrito/',carrito,name="carrito"),
]