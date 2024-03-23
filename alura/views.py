from django.shortcuts import render,redirect
from .models import (
    Categoria,Area,Curso,CursoImagen
)
#from django.http import HttpResponse

# Create your views here.
def paginaalura(request):
    return render(request,'home.html')

def index(request):
    lista_categorias = Categoria.objects.all()
    lista_areas = Area.objects.all()

    categoria_id = request.GET.get('cat')
    area_id = request.GET.get('are')
    if categoria_id:
        categoria_seleccionada = Categoria.objects.get(pk=categoria_id)
        lista_cursos = Curso.objects.filter(categoria=categoria_seleccionada)
    elif area_id:
        area_seleccionada = Area.objects.get(pk=area_id)
        lista_cursos = Curso.objects.filter(area=area_seleccionada)
    else:
        lista_cursos = Curso.objects.all()

    context = {
        'categorias':lista_categorias,
        'areas': lista_areas,
        'cursos': lista_cursos
    }
    
    return render(request, 'index.html',context)

def curso(request,curso_id):
    obj_curso = Curso.objects.get(pk=curso_id)
    context = {
        'curso':obj_curso
    }
    return render(request,'curso.html',context)

###carrito
from .cart import Cart

def carrito(request):
    return render(request, 'carrito.html')

def agregar_carrito(request,curso_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
    obj_curso = Curso.objects.get(pk=curso_id)
    curso_imagenes = CursoImagen.objects.filter(curso=obj_curso)
    print(curso_imagenes[0])

    carrito = Cart(request)
    carrito.add(obj_curso,cantidad,curso_imagenes[0].imagen.url)

    if request.method == 'GET':
        return redirect('/cursos')

    return render(request,'carrito.html')

def eliminar_carrito(request,curso_id):
    obj_curso = Curso.objects.get(pk=curso_id)
    carrito = Cart(request)
    carrito.delete(obj_curso)

    if request.GET.get('hd') =='1':
        return redirect('/cursos')

    return render(request,'carrito.html')

def limpiar_carrito(request):
    carrito = Cart(request)
    carrito.clear()

    return render(request, 'carrito.html')

###usuario y login ###
from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


def crear_usuario(request):
    if request.method== 'POST':
        data_usuario = request.POST['nuevo_usuario']
        data_password = request.POST['nuevo_password']

        obj_usuario = User.objects.create_user(username=data_usuario,password=data_password)

        if obj_usuario is not None:
            login(request,obj_usuario)
            return redirect('/cuenta')

    return render(request, 'login.html')

def login_usuario(request):
    
    pagina_destino = request.GET.get('next',None)
    context = {
        'destino':pagina_destino
    }
    if request.method== 'POST':
        data_usuario = request.POST['login_usuario']
        data_password= request.POST['login_password']
        data_destino = request.POST['destino']

        obj_usuario= authenticate(request,username=data_usuario,password=data_password)

        if obj_usuario is not None:
            login(request,obj_usuario)

            if data_destino != 'None':
                return redirect(data_destino)

            return redirect('/cuenta')
        else:
            context = {
                'mensajeError': 'Datos Incorrectos'
            }

    return render(request, 'login.html',context)

def logout_usuario(request):
    logout(request)
    return redirect('/')

####cliente####

from .models import Cliente
from .forms import ClienteForm

@login_required(login_url='/login')
def cuenta_usuario(request):
    data = {}

    if request.user.first_name != '':
        data.update({'nombre':request.user.first_name})

    if request.user.last_name != '':
        data.update({'apellidos':request.user.last_name})

    data.update({'email':request.user.username})

    ### cargamos datos cliente

    try:
        obj_cliente = Cliente.objects.get(usuario=request.user)
        data_cliente = {
            'direccion': obj_cliente.direccion,
            'telefono':obj_cliente.telefono,
            'dni':obj_cliente.dni,
            'fecha_nacimiento':obj_cliente.fecha_nacimiento,
            'sexo': obj_cliente.sexo
        }
    except:
        data_cliente = {
            'direccion': '',
            'telefono':'',
            'dni':'',
            'fecha_nacimiento':'',
            'sexo':'M'
        }

    data.update(data_cliente)


    form_cliente = ClienteForm(data)
    context={
        'frm_cliente':form_cliente
    }
    return render(request,'cuenta.html',context)

@login_required(login_url='/login')
def actualizar_cliente(request):
    if request.method== 'POST':
        frm_cliente = ClienteForm(request.POST)
        if frm_cliente.is_valid():
            data = frm_cliente.cleaned_data

            #update user
            obj_usuario = User.objects.get(pk=request.user.id)
            obj_usuario.first_name = data['nombre']
            obj_usuario.last_name = data['apellidos']
            obj_usuario.email=data['email']
            obj_usuario.save()

            try:
                obj_cliente = Cliente.objects.get(usuario=obj_usuario)
            except:
                obj_cliente = Cliente()
                obj_cliente.usuario = obj_usuario

            obj_cliente.dni = data['dni']
            obj_cliente.direccion = data['direccion']
            obj_cliente.telefono = data['telefono']
            obj_cliente.fecha_nacimiento = data['fecha_nacimiento']
            obj_cliente.sexo=data['sexo']
            obj_cliente.save()
            mensaje = 'Datos Guardados'

    return redirect('/cuenta')

###pedido###

from .models import Pedido,PedidoDetalle

@login_required(login_url='/login')
def pedido(request):
    data = {}

    if request.user.first_name != '':
        data.update({'nombre':request.user.first_name})

    if request.user.last_name != '':
        data.update({'apellidos':request.user.last_name})

    data.update({'email':request.user.username})

    ### cargamos datos cliente

    try:
        obj_cliente = Cliente.objects.get(usuario=request.user)
        data_cliente = {
            'direccion': obj_cliente.direccion,
            'telefono':obj_cliente.telefono,
            'dni':obj_cliente.dni,
            'fecha_nacimiento':obj_cliente.fecha_nacimiento,
            'sexo': obj_cliente.sexo
        }
    except:
        data_cliente = {
            'direccion': '',
            'telefono':'',
            'dni':'',
            'fecha_nacimiento':'',
            'sexo':'M'
        }

    data.update(data_cliente)


    form_cliente = ClienteForm(data)
    context={
        'frm_cliente':form_cliente
    }
    return render(request,'pedido.html',context)

from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

@login_required(login_url='/login')
def registrar_pedido(request):
    if request.method == 'POST':
        frm_cliente = ClienteForm(request.POST)
        if frm_cliente.is_valid():
            data = frm_cliente.cleaned_data

            #update user
            obj_usuario = User.objects.get(pk=request.user.id)
            obj_usuario.first_name = data['nombre']
            obj_usuario.last_name = data['apellidos']
            obj_usuario.email=data['email']
            obj_usuario.save()

            try:
                obj_cliente = Cliente.objects.get(usuario=obj_usuario)
            except:
                obj_cliente = Cliente()
                obj_cliente.usuario = obj_usuario

            obj_cliente.dni = data['dni']
            obj_cliente.direccion = data['direccion']
            obj_cliente.telefono = data['telefono']
            obj_cliente.fecha_nacimiento = data['fecha_nacimiento']
            obj_cliente.sexo=data['sexo']
            obj_cliente.save()

        #registrar pedido
        
        monto_total= float(request.session.get('cart_total'))
        obj_pedido = Pedido()
        obj_pedido.cliente = obj_cliente
        obj_pedido.save()
        nro_pedido = 'PEP' + obj_pedido.fecha_registro.strftime('%Y')+ str(obj_pedido.id)
        obj_pedido.nro_pedido = nro_pedido
        obj_pedido.save()

        carrito = request.session.get('cart')
        for key,value in carrito.items():
            obj_producto = Curso.objects.get(pk=value['curso_id'])
            obj_pedido_detalle = PedidoDetalle()
            obj_pedido_detalle.pedido = obj_pedido
            obj_pedido_detalle.producto = obj_producto
            obj_pedido_detalle.cantidad = int(value['cantidad'])
            obj_pedido_detalle.subtotal = float(value['subtotal'])
            obj_pedido_detalle.save()

        ## btn paypal
        paypal_dict = {
        "business": "sb-qyxr130010752@business.example.com",
        "amount": monto_total,
        "item_name": "PEDIDO NRO: " + obj_pedido.nro_pedido,
        "invoice": obj_pedido.id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('alura:gracias')),
        "cancel_return": request.build_absolute_uri(reverse('alura:index')),
        }

        # Create the instance.
        frm_paypal = PayPalPaymentsForm(initial=paypal_dict)
        context = {
            'pedido': obj_pedido,
            'frm_paypal':frm_paypal
        }

        request.session['pedido_id']= obj_pedido.id

        return render (request,'pago.html',context)

@login_required(login_url='/login')
def gracias(request):
    paypal_id = request.GET.get('PayerID',None)
    if paypal_id is not None:
        pedido_id = request.session.get('pedido_id')
        pedido = Pedido.objects.get(pk=pedido_id)
        pedido.estado = '1'
        pedido.save()

        request.session['pedido_id'] = None
        carrito = Cart(request)
        carrito.clear()

    return render(request,'gracias.html')

@login_required(login_url='/login')
def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-qyxr130010752@business.example.com",
        "amount": "100.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('alura:index')),
        "cancel_return": request.build_absolute_uri(reverse('alura:index')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)