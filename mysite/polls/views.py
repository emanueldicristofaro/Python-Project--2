from django.shortcuts import render
from .models import Tamano, Ingrediente, Bebida

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
