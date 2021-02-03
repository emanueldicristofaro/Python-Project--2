from django.shortcuts import render
from django.utils import timezone 
from .models import Pedido, Tamano, Ingrediente, Bebida, Sandwich, Sandwich_Ingrediente, Bebida_Sandwich


# Metodo para realizar el insert del pedido en el sistema
#######################################################################

pedido = list()
cliente_nombre = list()
def insertPedido(pedido, cliente):

    # Obtener fecha actual
    fechaActual = timezone.now()

    size = []
    ingredients = []
    drinks = []

    pedidoInsert = Pedido.objects.create(fechaPedido = fechaActual, nombreCliente = cliente)

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
    idCliente = Pedido.objects.filter(nombreCliente = cliente)[Pedido.objects.filter(nombreCliente = cliente).count()-1]
    idClienteUsar = idCliente.id_pedido    
        
    for s in size:
        sizeId = Tamano.objects.get(id_tamano = s)
        sandwich = Sandwich(fk_pedido = idCliente, fk_tamano = sizeId)
        sandwich.save()

    #Insert bebidas in sandwich

    listaSandwichesNueva = list()

    listaSandwiches = Sandwich.objects.all().filter(fk_pedido_id = idClienteUsar)

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

#######################################################################

# Metodo para calcular el monto total del pedido
#######################################################################

def cacularPrecio(pedido):
    lista_sandwiches = Sandwich.objects.all().filter(fk_pedido_id = pedido.id_pedido)
    precio = 0
    for sandwich in lista_sandwiches:
        tamano = Tamano.objects.get(id_tamano = sandwich.fk_tamano_id)
        lista_bebidas = Bebida_Sandwich.objects.all().filter(fk_sandwich_id = sandwich.id_sandwich)
        lista_ingredientes = Sandwich_Ingrediente.objects.all().filter(fk_sandwich_id = sandwich.id_sandwich)        
        for bebidas in lista_bebidas:
            bebida = Bebida.objects.get(id_bebida = bebidas.fk_bebida_id)
            precio += bebida.costoBebida
        for ingredientes in lista_ingredientes:
            ingrediente = Ingrediente.objects.get(id_ingrediente = ingredientes.fk_ingrediente_id)
            precio += ingrediente.costoIngrediente
        precio += tamano.costoTamano
    return precio

#######################################################################

# Metodo obtener los elementos del pedido para la factura
#######################################################################

def renderSandwiches(pedido):
    lista_sandwiches = Sandwich.objects.all().filter(fk_pedido_id = pedido.id_pedido)
    render_sandwiches = list()
    for sandwich in lista_sandwiches:
        precio = 0
        tamano = Tamano.objects.get(id_tamano = sandwich.fk_tamano_id)
        lista_bebidas = Bebida_Sandwich.objects.all().filter(fk_sandwich_id = sandwich.id_sandwich)
        lista_ingredientes = Sandwich_Ingrediente.objects.all().filter(fk_sandwich_id = sandwich.id_sandwich)
        render_bebidas = list()
        render_ingredientes = list()

        for bebidas in lista_bebidas:
            bebida = Bebida.objects.get(id_bebida = bebidas.fk_bebida_id)
            render_bebidas.append(bebida)
            precio += bebida.costoBebida

        for ingredientes in lista_ingredientes:
            ingrediente = Ingrediente.objects.get(id_ingrediente = ingredientes.fk_ingrediente_id)
            render_ingredientes.append(ingrediente)
            precio += ingrediente.costoIngrediente

        precio += tamano.costoTamano
        diccionario = {
            'sandwich' : sandwich.id_sandwich,
            'tamano' : tamano.nombreTamano,
            'tamano_precio' : tamano.costoTamano,
            'bebidas' : render_bebidas,
            'ingredientes' : render_ingredientes,
            'precio' : precio
        }
        render_sandwiches.append(diccionario)
    return render_sandwiches

#######################################################################

# Pagina principal para introducir el nombre del cliente
#######################################################################    

def index(request):
    #pedido = Pedido.objects.get(nombreCliente = req)
    return render(request, 'pedidos/index.html')

#######################################################################

# Pagina principal para que se traiga toda la data y las opciones de pedido
#######################################################################

def catalogo(request):
    
    if request.method == 'POST':
        if 'client' in request.POST:
            cliente = request.POST['client']
        else:
            cliente = cliente_nombre[0]
        tamano = request.POST.get("size")
        lista_ingredientes = request.POST.getlist('ingredients')
        lista_bebidas = request.POST.getlist('drinks')

        if request.POST.get("actionbtn") == "end":
            
            #Realizar el insert
            pedido.pop(0)           
            pedidoId = insertPedido(pedido, cliente_nombre[0])            
            total = cacularPrecio(pedidoId)
            sanduches = renderSandwiches(pedidoId)
            context = { 'pedidoId' : pedidoId, 'total' : total, 'sanduches' : sanduches}

            # render para detalles del pedido
            pedido.clear()
            cliente_nombre.clear()

            # Redirigir a la pagina de fatura
        
            return render(request, 'pedidos/factura.html', context)

        else:
            cliente_nombre.append(cliente)
            sandwich = {
                #"client": cliente,
                "size": tamano,
                "ingredients": lista_ingredientes,
                "drinks": lista_bebidas
            }

            pedido.append(sandwich)

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

    raw_query = '''SELECT polls_pedido.id_pedido, polls_pedido.nombreCliente as nombre, polls_pedido.fechaPedido as fecha, 
    ((count(polls_tamano.nombreTamano) * polls_tamano.costoTamano) + (count(polls_bebida.nombreBebida) * polls_bebida.costoBebida) + (count(polls_ingrediente.nombreIngrediente) * polls_ingrediente.costoIngrediente)) as monto
    FROM polls_pedido, polls_sandwich, polls_bebida, polls_tamano, polls_bebida_sandwich, polls_sandwich_ingrediente, polls_ingrediente
    WHERE polls_pedido.id_pedido = polls_sandwich.fk_pedido_id and polls_sandwich.fk_tamano_id = polls_tamano.id_tamano and 
    polls_sandwich.id_sandwich = polls_sandwich_ingrediente.fk_sandwich_id and polls_sandwich_ingrediente.fk_ingrediente_id = polls_ingrediente.id_ingrediente and 
    polls_sandwich.id_sandwich = polls_bebida_sandwich.fk_sandwich_id and polls_bebida_sandwich.fk_bebida_id = polls_bebida.id_bebida
    GROUP BY polls_pedido.nombreCliente'''
    
    results = Pedido.objects.raw(raw_query)

    return render(request, 'pedidos/ventas.html', {'resultado': results})

#######################################################################

# Ventas por dias
#######################################################################

def ventasDias(request):

    tamanoQuery = ''' SELECT polls_pedido.id_pedido, polls_pedido.fechaPedido as FechaTamano, sum(polls_tamano.costoTamano) as MontoTamano, polls_tamano.nombreTamano as nombreTamano 
                FROM polls_pedido, polls_tamano, polls_sandwich 
                WHERE polls_pedido.id_pedido = polls_sandwich.fk_pedido_id and polls_sandwich.fk_tamano_id = polls_tamano.id_tamano
                GROUP BY polls_pedido.fechaPedido, polls_tamano.nombreTamano '''

    tamanoResults = Pedido.objects.raw(tamanoQuery)

    ingredienteQuery = '''SELECT polls_pedido.id_pedido, polls_pedido.fechaPedido as fechaIngrediente, sum(polls_ingrediente.costoIngrediente) as montoIngrediente, polls_ingrediente.nombreIngrediente as nombreIngrediente 
                        FROM polls_pedido, polls_ingrediente, polls_sandwich, polls_sandwich_ingrediente
                        WHERE polls_pedido.id_pedido = polls_sandwich.fk_pedido_id and polls_sandwich.id_sandwich = polls_sandwich_ingrediente.fk_sandwich_id and 
                        polls_sandwich_ingrediente.fk_ingrediente_id = polls_ingrediente.id_ingrediente
                        GROUP BY polls_pedido.fechaPedido, polls_ingrediente.nombreIngrediente'''

    ingredienteResults = Pedido.objects.raw(ingredienteQuery)

    bebidaQuery = '''SELECT polls_pedido.id_pedido, polls_pedido.fechaPedido as fechaBebida, sum(polls_bebida.costoBebida) as montoBebida, polls_bebida.nombreBebida as nombreBebida
                    FROM polls_pedido, polls_bebida, polls_sandwich, polls_bebida_sandwich
                    WHERE polls_pedido.id_pedido = polls_sandwich.fk_pedido_id and polls_sandwich.id_sandwich = polls_bebida_sandwich.fk_sandwich_id and 
                    polls_bebida_sandwich.fk_bebida_id = polls_bebida.id_bebida
                    GROUP BY polls_pedido.fechaPedido, polls_bebida.nombreBebida'''

    bebidaResults = Pedido.objects.raw(bebidaQuery)

    return render(request, 'pedidos/ventas_dias.html', {'tamanos': tamanoResults, 'ingredientes': ingredienteResults, 'bebidas': bebidaResults})

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
                group by polls_tamano.nombreTamano
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

