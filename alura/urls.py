from django.urls import path
from . import views

app_name = 'alura'

urlpatterns =[
    path('cursos',views.index,name='index'),
    path('curso/<int:curso_id>',views.curso,name='curso'),
    path('carrito',views.carrito,name='carrito'),
    path('carrito/add/<int:curso_id>',views.agregar_carrito,name='agregarcarrito'),
    path('carrito/del/<int:curso_id>',views.eliminar_carrito,name='eliminarcarrito'),
    path('carrito/clear',views.limpiar_carrito,name='limpiarcarrito'),
    path('usuario/add',views.crear_usuario,name='crearusuario'),
    path('cuenta',views.cuenta_usuario,name='cuentausuario'),
    path('login',views.login_usuario,name='loginusuario'),
    path('salir',views.logout_usuario,name='logoutusuario'),
    path('cliente/update',views.actualizar_cliente,name='actualizarcliente'),
    path('pedido',views.pedido,name='pedido'),
    path('pedido/add',views.registrar_pedido,name='registrar_pedido'),
    path('paypaltest',views.view_that_asks_for_money,name='paypaltest'),
    path('gracias',views.gracias,name='gracias'),
    path('',views.paginaalura,name='home'),
]