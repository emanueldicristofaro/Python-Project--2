from django.shortcuts import render
from django.utils import timezone 
from .models import Pedido, Tamano, Ingrediente, Bebida, Sandwich, Sandwich_Ingrediente, Bebida_Sandwich


# Pagina principal para que se traiga toda la data y las opciones de pedido
#######################################################################

pedido = list()

def insertPedido(pedido, cliente):

    # Obtener fecha actual
    fechaActual = timezone.now()

    size = []
    ingredients = []
    drinks = []

    pedidoInsert = Pedido.objects.create(fechaPedido = fechaActual, nombreCliente = "Emanuel")

    #Operaciones de insert
    for pe in pedido:

        for key, value in pe.items():

           if key == "size":
               
              size.append(value)

           elif key == "ingredients":

              ingredients.append(value)

           elif key == "drinks":

              drinks.append(value)

    #Insert in sandwich 
    idCliente = Pedido.objects.get(nombreCliente = "Emanuel")
    nombreClienteString = idCliente.nombreCliente    
        
    for s in size:
        sizeId = Tamano.objects.get(id_tamano = s)
        sandwich = Sandwich(fk_pedido = idCliente, fk_tamano = sizeId)
        sandwich.save()

    #Insert bebidas in sandwich

    QuerySandwichs = '''SELECT polls_sandwich.id_sandwich FROM polls_sandwich 
    WHERE polls_sandwich.fk_pedido_id = (SELECT polls_pedido.id_pedido FROM polls_pedido WHERE polls_pedido.nombreCliente = %s)'''

    listaSandwiches = Sandwich.objects.raw(QuerySandwichs, [nombreClienteString])
    listaSandwichesNueva = list()

    for sand in listaSandwiches:
        listaSandwichesNueva.append(sand.id_sandwich)

    contador = 0
    #Procedure 
    for b in drinks:

        for bed in b:

            drinkId = Bebida.objects.get(id_bebida = bed)
            sandwichId = Sandwich.objects.get(id_sandwich = listaSandwichesNueva[contador])
            sandwich_bebida = Bebida_Sandwich(fk_sandwich = sandwichId, fk_bebida = drinkId)
            sandwich_bebida.save()
            
        contador = contador + 1

    #Insert ingredientes in sandwich

    contador_2 = 0
    #Procedure
    for i in ingredients:

        for ing in i:

            ingredientId = Ingrediente.objects.get(id_ingrediente = ing)
            sandwichId = Sandwich.objects.get(id_sandwich = listaSandwichesNueva[contador_2])
            ingredientes_sandwiches = Sandwich_Ingrediente(fk_sandwich = sandwichId, fk_ingrediente = ingredientId)
            ingredientes_sandwiches.save()

        contador_2 = contador_2 + 1

    #########################################
    #Resetear las listas
    size.clear()
    ingredients.clear()
    drinks.clear()
    contador = 0
    contador_2 = 0
    listaSandwichesNueva.clear()
    #########################################
      
    return idCliente

def index(request):
    return render(request, 'pedidos/index.html')

def catalogo(request):

    cliente = request.POST['client']

    if request.method == 'POST':

        tamano = request.POST.get("size")
        lista_ingredientes = request.POST.getlist('ingredients')
        lista_bebidas = request.POST.getlist('drinks')

        if request.POST.get("actionbtn") == "end":
            
            #Realizar el insert

            context = insertPedido(pedido, cliente)

            # render para detalles del pedido
            pedido.clear()
            print("post")

            # Redirigir a la pagina de fatura
        
            return render(request, 'pedidos/factura.html')

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
    return render(request, 'pedidos/catalogo.html', contex)

#######################################################################

# Factura
#######################################################################

def factura(request, pedido):

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

    raw_query = '''
                select polls_ingrediente.id_ingrediente, polls_ingrediente.nombreIngrediente AS Nombre, 
                count(polls_ingrediente.id_ingrediente) AS Cantidad,
                count(polls_ingrediente.id_ingrediente) * polls_ingrediente.costoIngrediente AS Monto
                from polls_ingrediente , polls_sandwich , polls_sandwich_ingrediente 
                where polls_sandwich_ingrediente.fk_sandwich_id = polls_sandwich.id_sandwich 
                 and polls_sandwich_ingrediente.fk_ingrediente_id = polls_ingrediente.id_ingrediente
                group by polls_ingrediente.nombreIngrediente
        '''
    
    results = Ingrediente.objects.raw(raw_query)
    return render(request, 'pedidos/ventas_ingredientes.html', {'resultado': results})

#######################################################################

# Ventas por tamano
#######################################################################

def ventasTamano(request):

    raw_query = '''
                select polls_pedido.id_pedido, 
                polls_tamano.nombreTamano Nombre, 
                count(polls_sandwich.fk_tamano_id) Cantidad,
                count(polls_sandwich.fk_tamano_id) * polls_tamano.costoTamano Monto
                from  polls_pedido , polls_sandwich, polls_tamano 
                where polls_sandwich.fk_pedido_id = polls_pedido.id_pedido and
                polls_sandwich.fk_tamano_id = polls_tamano.id_tamano
                group by polls_tamano.nombreTamano
        '''
    
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pedidos/ventas_tamanos.html', {'resultado': results})

#######################################################################

# Ventas por tamano
#######################################################################

def ventasClientes(request):

    raw_query = '''
                select polls_pedido.id_pedido, 
                polls_pedido.nombreCliente Cliente,
                polls_tamano.nombreTamano Tamano, 
                count(polls_sandwich.fk_tamano_id) Cantidad,
                count(polls_sandwich.fk_tamano_id) * polls_tamano.costoTamano Monto
                from polls_pedido , polls_sandwich, polls_tamano 
                where polls_sandwich.fk_pedido_id = polls_pedido.id_pedido and
                polls_sandwich.fk_tamano_id = polls_tamano.id_tamano
                group by polls_pedido.nombreCliente
        '''
    
    results = Pedido.objects.raw(raw_query)
    return render(request, 'pedidos/ventas_clientes.html', {'resultado': results})

#######################################################################

# Ventas por bebidas
#######################################################################

def ventasBebidas(request):

    raw_query = '''
                select polls_bebida.id_bebida, polls_bebida.nombreBebida AS Nombre, 
                count(polls_bebida.id_bebida) AS Cantidad,
                count(polls_bebida.id_bebida) * polls_bebida.costoBebida AS Monto
                from polls_bebida , polls_sandwich , polls_bebida_sandwich
                where polls_bebida_sandwich.fk_sandwich_id = polls_sandwich.id_sandwich 
                 and polls_bebida_sandwich.fk_bebida_id = polls_bebida.id_bebida
                group by polls_bebida.nombreBebida
        '''
    
    results = Bebida.objects.raw(raw_query)
    return render(request, 'pedidos/ventas_bebidas.html', {'resultado': results})

#######################################################################

