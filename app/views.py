from genericpath import exists
from math import prod
from urllib import response
import requests #NOS PERMITE LEER EL API
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render,redirect
from django.contrib import messages
from.forms import *
from.models import *
# Create your views here.

def index (request):
    return render(request, 'app/index.html')

def registrar(request):
    datos = {
        'form' : formularioRegistro()
    }
    if request.method == 'POST':
        formulario = formularioRegistro(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            #user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            #login(request,user)
            #messages.success(request,'Registrado correctamente!')
            #User.groups.add(Empleado)
            #return redirect(to="home")
        datos["form"] = formulario

    return render(request, 'app/registration/register.html', datos)

def solicitud_servicio(request):
    return render(request, 'app/solicitud_servicio.html')

def productos(request):
        response = requests.get('').json()
        datos = {'listaJson' : response}
        cid = request.user.id
        carritoAll= Items_Carrito.objects.all()
        productoALL= Producto.objects.all()
        datos ={'lista_Productos' :productoALL,
                'carro': carritoAll,
                'id': cid,
                } 

        if request.method == 'POST':
            tipo= TipoProducto()
            tipo.tipo =request.POST.get('tipo_producto')

            producto = Producto()
            producto.codigo = request.POST.get('codigo_producto')
            producto.nombre = request.POST.get('nombre_producto')
            producto.marca = request.POST.get('marca_producto')
            producto.precio = request.POST.get('precio_producto')
            producto.descripcion = request.POST.get('descripcion_producto')
            producto.stock = request.POST.get('stock_producto')
            producto.imagen = request.POST.get('imagen_producto')
            producto.tipo = tipo
            

            carrito = Items_Carrito()
            carrito.user = cid
            carrito.cantidad = 0
            var_estado = True
            if Items_Carrito.objects.filter(producto=request.POST.get('codigo_producto')).exists():
                for n in carritoAll:
                    if n.producto.nombre == producto.nombre:
                        n.cantidad = n.cantidad + 1
                        n.save()
                        var_estado = False 
            else:
                carrito.producto = producto
                carrito.cantidad = 1
                carrito.save()
                var_estado = False
                
            if var_estado == True:
                carrito.producto = producto
                carrito.cantidad = 1
                carrito.save()
            
            
            codigo = request.POST.get('codigo_producto')
            productoA = Producto.objects.get(codigo=codigo)
            if productoA == Producto.objects.get(codigo=codigo):
                if productoA.stock > 0:
                    productoA.stock = productoA.stock -1
                    productoA.save()
                else:
                    producto.stock == 0
                    productoA.delete()
        return render(request, 'app/productos.html', datos)

def historial(request):
    historial_compra= Despacho.objects.filter(usuario=id)
    productos_compra=Items_Despacho.objects.filter(id_user = id)
    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra}
    return render(request, 'app/historial.html',datos)

def despacho(request):
    historial_compra= Despacho.objects.filter(usuario=id)
    productos_compra=Items_Despacho.objects.filter(id_user = id)
    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra}
    return render(request, 'app/despacho.html',datos)

def carrito(request):
    carrito= Items_Carrito.objects.filter(user=id)

    datos={ 'listar_carrito' :carrito,
            'usuario': 0,
    }
    lista = carrito
    datos['total']=0

    usuario = request.user.username
    usuario_id = request.user.id
    susvalida=Suscripcion.objects.filter(username=usuario).get()
    if susvalida.is_suscrito == True:
        datos['usuario'] = 1
        for cart in lista:
            datos['totalsub']= round((cart.producto.precio * cart.cantidad +datos['total'])*0.95)
            datos['total']= cart.producto.precio * cart.cantidad + datos['total']
            datos['descuento']=round(datos['total']*0.05)
    else:
        datos['usuario'] = 0
        for cart in lista:
            datos['total']= cart.producto.precio * cart.cantidad + datos['total']
            datos['no_sus']="Debes estar suscrito"
  
    if request.method == 'POST':
        compra= Despacho()
        compra.usuario = usuario_id
        if susvalida.is_suscrito == True:
            compra.total_compra= datos['totalsub']
        else:
            compra.total_compra= datos['total']
        compra.estado ="pago verificado"
        compra.save()
        compraid=compra.id

        for n in carrito:
            despacho = Items_Despacho()

            despacho.cantidad = n.cantidad
            despacho.producto = n.producto
            despacho.id_user = n.user
            despacho.id_pago = compraid
            despacho.save()
        
        carrito.delete()
        datos['mensaje'] = 'pago verificado'
        messages.success(request,'Pago realizado con exito')

        return render(request,'carrito.html',datos)