from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('factura/', views.factura, name='factura'),
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/dias', views.ventasDias, name='ventasDias'),
    path('ventas/ingredientes', views.ventasIngredientes, name='ventasIngredientes'),
    path('ventas/tamanos', views.ventasTamano, name='ventasTamanos'),
    path('ventas/clientes', views.ventasClientes, name='ventasClientes'),
]