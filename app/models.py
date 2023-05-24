from django.db import models

# Create your models here.
class Tipo_Producto(models.Model):
    Id_Tipo_Producto = models.IntegerField(null=False,primary_key=True)
    Tipo_Producto = models.CharField(max_length=50)
    Descripcion = models.TextField()

    def __str__(self):
        return self.Id_Tipo_Producto
    class Meta:
        db_table = 'db.Tipo_Producto'

class Producto(models.Model):
    Id_Producto = models.IntegerField(null=False,primary_key=True)
    Nombre = models.CharField(max_length=50)
    Stock =  models.IntegerField()
    Descripcion = models.TextField()
    Imagen = models.ImageField()
    Tipo_Producto = models.ForeignKey(Tipo_Producto, on_delete=models.CASCADE)
    Precio = models.IntegerField()

    def __str__(self):
        return self.Id_Producto
    class Meta:
        db_table = 'db.Producto'

class Solicitud_Servicio(models.Model):
    Id_solicitud = models.IntegerField(null=False, primary_key=True)
    usuario = models.IntegerField()
    Producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    Descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_servicio = models.DateField()

    def __str__(self):
        return self.Id_solicitud
    class Meta:
        db_table = 'db.Solicitud_Servicio'


class Historial_Compra(models.Model):
    id_historic = models.IntegerField(null=False, primary_key=True)
    usuario = models.IntegerField()
    fecha_compra = models.DateField(auto_now_add=True)
    estado_despacho = models.CharField(max_length= 500)
    total = models.IntegerField()

    
    def __str__(self):
        return self.id_historic
    class Meta:
        db_table = 'db.Historial_Compra'

class Boleta_Compra(models.Model):
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.IntegerField()
    cantidad = models.IntegerField()
    id_compra = models.IntegerField()

    def __str__(self):
        return self.id_compra
    class Meta:
        db_table = 'db.Boleta_Compra'
    
class Historial_Servicio(models.Model):
    id_historic2 = models.IntegerField(null=False, primary_key=True)
    usuario = models.IntegerField()
    servicio = models.ForeignKey(Solicitud_Servicio, on_delete=models.CASCADE)
    fecha_solicitud =models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=30)
    fecha_modificacion = models.DateField(auto_now=True)

    def __str__(self):
        return self.id_historic2
    class Meta:
        db_table = 'db.Historial_Servicio'

class items_carrito(models.Model):
    id_carrito = models.IntegerField(null= False,primary_key=True)
    usuario = models.IntegerField()
    cantidad = models.IntegerField()
    total = models.IntegerField()
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)
