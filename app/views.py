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
    response = requests.get('https://localhost:7292/api/productos',verify=False).json()
    datos={
        'form' : formularioSolicitudServ(),
        'lista_productos' : response
          }
    user = request.user.id
    if request.method == 'POST':
        print('Primer paso')
        print(user)
        formulario = formularioSolicitudServ(request.POST,files=request.FILES, initial={'usuario':'0'})
        

        if formulario.is_valid():
            #formulario.cleaned_data["usuario"] = user
            print('es valido')
            fs=formulario.save(commit=False)
            fs.usuario = user
            fs.save()

            historial_servicios = Historial_Servicio()
            historial_servicios.servicio = fs
            historial_servicios.usuario = user
            historial_servicios.estado = "En curso"
            historial_servicios.save()
           
            messages.success(request,'Solicitud enviada correctamente!')

    return render(request, 'app/solicitud_servicio.html',datos)

@login_required
def productos(request):
        response = requests.get('https://localhost:7292/api/productos',verify=False).json()
        responseTipo = requests.get('https://localhost:7292/api/tipoProductos',verify=False).json()


        cid = request.user.id
      
        carritoAll= items_carrito.objects.filter(usuario= cid)
        ##productoALL= Producto.objects.all() 
        datos ={'lista_Productos' :response,#productoALL,
                'lista_Tipo' :responseTipo,#carritoAll,
                'carro': carritoAll,
                'id': cid,
                } 

        if request.method == 'POST':
            print('post post post')
            producto = Producto()
            producto.Id_producto = request.POST.get('id_producto')
            producto.precio = request.POST.get('precio')
            producto.save()

            carrito = items_carrito()
            carrito.usuario = cid
            carrito.cantidad = 0

            pro = []

            for n in carritoAll:
                pro.append(n.productos.Id_producto)

            if pro:
                print('en primer')
                for n in pro:
                    if n == int(request.POST.get('id_producto')):
                        print('en segundo')
                        for n in carritoAll:
                            if n.productos.Id_producto == int(producto.Id_producto):
                                print(n.cantidad)
                                n.cantidad += 1
                                print(n.cantidad)
                                print('en el tercer if')
                                n.save()
                
            else:
                print('en el else')
                carrito.productos = producto
                carrito.cantidad = 1
                carrito.save()
                
        return render(request, 'app/productos.html',datos) #datos)

@login_required
def carrito(request, id):
    response = requests.get('https://localhost:7292/api/productos',verify=False).json()
    responseTipo = requests.get('https://localhost:7292/api/tipoProductos',verify=False).json()
    carrito= items_carrito.objects.filter(usuario=id)

    datos={ 'listar_carrito' :carrito,
           'lista_productos':response,
           'lista_tipo':responseTipo
    }
    lista = carrito
    datos['total']=0

    usuario_id = request.user.id
    for cart in lista:
            datos['total']= cart.productos.precio * cart.cantidad + datos['total']
  
    if request.method == 'POST':
        compra= Historial_Compra()
        compra.usuario = usuario_id
        compra.total= datos['total']
        compra.estado_despacho ="pago verificado"
        compra.save()
        compraid=compra.id

        for n in carrito:
            despacho = Boleta_Compra()

            despacho.cantidad = n.cantidad
            despacho.productos = n.productos
            despacho.usuario = n.usuario
            despacho.id_compra = compraid
            despacho.save()
        carrito.delete()

    return render(request,'app/carrito.html',datos)

#################################################################
#UX vistas
@login_required
def despacho(request):
    response = requests.get('https://localhost:7292/api/productos',verify=False).json()
    responseTipo = requests.get('https://localhost:7292/api/tipoProductos',verify=False).json()

    id= request.user.id

    historial_compra= Historial_Compra.objects.filter(usuario=id)
    productos_compra= Boleta_Compra.objects.filter(usuario=id)
    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra,
            'lista_items':response,}
    
    return render(request, 'app/despacho.html',datos)

@login_required
def perfil(request):
    return render(request, 'app/perfil.html')

@login_required
def historial_productos(request, id):
    response = requests.get('https://localhost:7292/api/productos',verify=False).json()
    responseTipo = requests.get('https://localhost:7292/api/tipoProductos',verify=False).json()

    historial_compra= Historial_Compra.objects.filter(usuario=id)
    productos_compra=Boleta_Compra.objects.filter(usuario=id)

    datos={'lista_historial':historial_compra,
            'lista_productos':productos_compra,
            'lista_items':response,
            'lista_tipo':response}
    
    return render(request, 'app/historial_productos.html', datos)

@login_required
def historial_servicios(request, id):
        
    solicitudes = Solicitud_Servicio.objects.filter(usuario=id)
    historial_servicios = Historial_Servicio.objects.filter(usuario=id)
    datos ={ 
            'solicitud' : solicitudes,
            'historial' : historial_servicios,
            }
    
    return render(request,'app/historial_servicios.html',datos)

@login_required
def bandeja_entrada (request):
    solicitudes = Solicitud_Servicio.objects.all()
    historiales =Historial_Servicios.objets.all()

    if request.method == 'POST':
        solicitud = Historial_Servicio.objects.get(id=request.POST.get('id'))
        solicitud.estado = request.POST.get('selecciona')
        solicitud.save()


    datos = {
            'solicitudes':solicitudes,
            'historiales':historiales,
            'usuario':0
    }
    return render(request,'app/bandeja_entrada.html',datos)

@login_required
def estado_servicio(request):

    return render(request, 'app/estado_servicio.html')

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