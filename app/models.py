from django.db import models

# Create your models here.

class Producto(models.Model):
    Id_producto = models.IntegerField(primary_key=True, null=False)  
    precio = models.IntegerField(null=True) 

    def __str__(self):
        return f'{self.Id_producto}'
    class Meta:
        db_table = 'db.Producto'

class Solicitud_Servicio(models.Model):
    usuario = models.IntegerField(null=True)
    Producto = models.IntegerField(null=True)
    Descripcion = models.TextField(null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_servicio = models.DateField()

    def __str__(self):
        return self.Id_solicitud
    class Meta:
        db_table = 'db.Solicitud_Servicio'


class Historial_Compra(models.Model):

    usuario = models.IntegerField(null=True)
    fecha_compra = models.DateField(auto_now_add=True)
    estado_despacho = models.CharField(max_length= 500)
    total = models.IntegerField(null=True)

    
    def __str__(self):
        return self.id_historic
    class Meta:
        db_table = 'db.Historial_Compra'
    
class Historial_Servicio(models.Model):
    usuario = models.IntegerField(null=True)
    servicio = models.ForeignKey(Solicitud_Servicio, on_delete=models.DO_NOTHING,db_constraint=False)
    fecha_solicitud =models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=30)
    fecha_modificacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.estado
    class Meta:
        db_table = 'db.Historial_Servicio'

class items_carrito(models.Model):

    usuario = models.IntegerField(null=True)
    productos = models.ForeignKey(Producto, on_delete=models.DO_NOTHING,db_constraint=False)
    cantidad = models.IntegerField(null=True)
    total = models.IntegerField(null=True)

    class Meta:
        db_table = 'db.Items_carrito'
    
class Boleta_Compra(models.Model):
    productos = models.ForeignKey(Producto, on_delete=models.DO_NOTHING,db_constraint=False)
    usuario = models.IntegerField(null=True)
    cantidad = models.IntegerField(null=True)
    id_compra = models.IntegerField(null=True)

    class Meta:
        db_table = 'db.Boleta_Compra'