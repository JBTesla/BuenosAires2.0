import uuid
from genericpath import exists
from math import prod
from urllib import response
import requests #API REST
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render,redirect
from django.contrib import messages
from.forms import *
from.models import *
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
#################################################
#Index principal
def index (request):
    return render(request, 'app/index.html')
#################################################
#Registration
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

    return render(request, 'registration/registro.html', datos)

##################################################33
#UX formularios y POST
@login_required
def solicitud_servicio(request):
    datos={
        'form' : formularioSolicitudServ()
          }
    if request.method == 'POST':
        formulario= formularioSolicitudServ(request.POST, files=request.FILES)
    if formulario.is_valid():
        formulario.save()
        messages.success(request,'Solicitud enviada correctamente!')
    return render(request, 'app/solicitud_servicio.html',datos)

@login_required
def productos(request):
        response = requests.get('https://localhost:7292/api/productos').json()
        responseTipo = requests.get('https://localhost:7292/api/tipoProductos').json()


        cid = request.user.id
        carritoAll= items_carrito.objects.all()
        ##productoALL= Producto.objects.all() 
        datos ={'lista_Productos' :response,#productoALL,
                'lista_Tipo' :responseTipo,#carritoAll,
                'carro': carritoAll,
                'id': cid,
                } 

        if request.method == 'POST':
            tipo= Tipo_Producto()
            tipo.Tipo_Producto = request.POST.get('tipo_Producto')

            producto = Producto()
            producto.Id_Producto = request.POST.get('codigo_producto')
            producto.nombre = request.POST.get('nombre_producto')
            producto.precio = request.POST.get('precio_producto')
            producto.descripcion = request.POST.get('descripcion_producto')
            producto.stock = request.POST.get('stock_producto')
            producto.imagen = request.POST.get('imagen_producto')
            producto.tipo = tipo
            

            carrito = items_carrito()
            carrito.user = cid
            carrito.cantidad = 0
            var_estado = True
            if items_carrito.objects.filter(producto=request.POST.get('codigo_producto')).exists():
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
        return render(request, 'app/productos.html',datos) #datos)

@login_required
def carrito(request, id):

    carrito= items_carrito.objects.filter(user=id)

    datos={ 'listar_carrito' :carrito,
    }
    lista = carrito
    datos['total']=0

    usuario_id = request.user.id
    for cart in lista:
            datos['total']= cart.productos.Precio * cart.cantidad + datos['total']
  
    if request.method == 'POST':
        compra= Historial_Compra()
        compra.id_historic =+1
        compra.usuario = usuario_id
        compra.total= datos['total']
        compra.estado_despacho ="pago verificado"
        compra.save()
        compraid=compra.id_historic

        for n in carrito:
            despacho = Boleta_Compra()

            despacho.cantidad = n.cantidad
            despacho.productos = n.productos
            despacho.usuario = n.usuario
            despacho.id_compra = compraid
            despacho.save()
        carrito.delete()
        return redirect('proccess_payment')
    return render(request,'app/carrito.html',datos)
    
def proccess_payment(request):
        host = request.get.host()
        paypal_dict ={
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '20.00',
            'item_name':str(uuid.uuid4()),
            'currency_code':'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'htto://{host}{reverse("paypal-return")}',
            'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context ={'form':form}
        return render(request, 'app/proccess_payment')
    
def paypal_return(request):
        messages.success(request, 'Tu pago se realizo con exito')
        return redirect('historial_productos')
    
def paypal_cancel(request):
        messages.error(request, 'Tu pago se cancelo')
        return redirect('carrito')

#################################################################
#UX vistas
@login_required
def despacho(request):
    historial_compra= Historial_Compra.objects.filter(usuario=id)
    productos_compra= Boleta_Compra.objects.filter(id_user = id)
    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra}
    return render(request, 'app/despacho.html',datos)

@login_required
def perfil(request):
    return render(request, 'app/perfil.html')

@login_required
def historial_productos(request, id):

    historial_compra= Historial_Compra.objects.filter(usuario=id)
    productos_compra=Boleta_Compra.objects.filter(id_user = id)
    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra}
    
    return render(request, 'app/historial_productos', datos)

@login_required
def historial_servicios(request, id):
        
    solicitudes = Solicitud_Servicio.objects.all()
    datos ={ 
            'bandejaEntrada' : solicitudes,
            }
    return render(request,'app/historial_servicios',datos)

@login_required
def bandeja_entrada (request):
    solicitudes = Solicitud_Servicio.objects.all()
    datos ={ 
            'bandejaEntrada' : solicitudes,
            }
    return render(request,'app/bandeja_entrada',datos)

@login_required
def empresas_servicios(request):

    responseInfo = requests.get('https://localhost:7292/api/info_prod_serv').json()
    responseTipoinfo =  requests.get('https://localhost:7292/api/tipo_serv_prov').json()
    
    datos ={
        'Info': responseInfo,
        'tipoInfo' : responseTipoinfo,
    }
    return render(request,'app/empresas_servicios.html',datos)

@login_required
def detalles_proveedor(request):
    responseInfo = requests.get('https://localhost:7292/api/info_prod_serv').json()
    responseTipoinfo =  requests.get('https://localhost:7292/api/tipo_serv_prov').json()
    
    datos ={
        'Info': responseInfo,
        'tipoInfo' : responseTipoinfo,
    }
    return render(request,'app/detalles_proveedor.html',datos)
#####################################################