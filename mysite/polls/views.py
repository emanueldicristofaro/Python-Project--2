from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida, Sandwich, Sandwich_Ingrediente, Bebida_Sandwich


# Pagina principal para que se traiga toda la data y las opciones de pedido
#######################################################################

pedido = list()

def index(request):

    if request.method == 'POST':

        tamano = request.POST.get("size")
        lista_ingredientes = request.POST.getlist('ingredients')
        lista_bebidas = request.POST.getlist('drinks')

        if request.POST.get("actionbtn") == "end":
            # render para detalles del pedido
            pedido.clear()
            print("post")
        else:
            sandwich = {
                "size": tamano,
                "ingredients": lista_ingredientes,
                "drinks": lista_bebidas
            }
            pedido.append(sandwich)
            print(pedido)

    tamanos = Tamano.objects.all()
    ingredientes = Ingrediente.objects.all()
    bebidas = Bebida.objects.all()
    contex = {'tamanos': tamanos, 'ingredientes': ingredientes, 'bebidas' : bebidas}
    return render(request, 'pedidos/index.html', contex)

#######################################################################

# Factura
#######################################################################

def factura(request):

    return render(request, 'pedidos/factura.html')

#######################################################################

# Ventas
#######################################################################

def ventas(request):

    return render(request, 'pedidos/ventas.html')

#######################################################################

# Ventas por dias
#######################################################################

def ventasDias(request):

    return render(request, 'pedidos/ventas_dias.html')

#######################################################################

# Ventas por ingredientes
#######################################################################

def ventasIngredientes(request):

    return render(request, 'pedidos/ventas_ingredientes.html')

#######################################################################

# Ventas por tamano
#######################################################################

def ventasTamano(request):

    return render(request, 'pedidos/ventas_tamanos.html')

#######################################################################

# Ventas por tamano
#######################################################################

def ventasClientes(request):

    return render(request, 'pedidos/ventas_clientes.html')

#######################################################################

