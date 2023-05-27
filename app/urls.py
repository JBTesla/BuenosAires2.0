from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('registrar/', registrar, name="registrar"),
    path('perfil/', perfil, name="perfil"),
    path('historial_productos/<id>/', historial_productos, name="historial_productos"),
    path('historial_servicios/<id>/', historial_servicios, name="historial_servicios"),
    path('empresas_servicios/', empresas_servicios, name="empresas_servicios"),
    path('detalles_proveedor/', detalles_proveedor, name="detalles_proveedor"),
    path('productos/', productos, name="productos"),
    path('carrito/<id>/', carrito, name="carrito"),
    path('solicitud_servicio/', solicitud_servicio, name="solicitud_servicio"),
    path('despacho/', despacho, name="despacho"),
    #paypal
    path('proccess_payment/', proccess_payment, name="proccess_payment"),
    path('paypal-return', paypal_return, name="paypal-return"),
    path('paypal-cancel', paypal_cancel, name="paypal-cancel")

]