from django.db import models

# Tabla tamaño para almacenar los tamaños de los sandwiches
#######################################################################

class Tamano(models.Model):

    id_tamano = models.AutoField(primary_key=True)
    nombreTamano = models.CharField(max_length=300)
    costoTamano = models.DecimalField(max_digits=15, decimal_places=2)

    def getNombreTamano(self):
        return self.nombreTamano

    def getCostoTamano(self):
        return self.costoTamano

    def __str__(self):
        return self.nombreTamano + " | " + str(self.costoTamano)

#######################################################################

# Tabla ingrediente para almacenar los ingredientes de los sandwiches
#######################################################################
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombreIngrediente = models.CharField(max_length=300)
    costoIngrediente = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def getNombreIngrediente(self):
        return self.nombreIngrediente

    def getCostoIngrediente(self):
        return self.costoIngrediente
        
    def __str__(self):
        return self.nombreIngrediente + " | " + str(self.costoIngrediente)

#######################################################################

# Tabla bebida para almacenar las bebidas de los pedidos
#######################################################################
class Bebida(models.Model):
    id_bebida = models.AutoField(primary_key=True)
    nombreBebida = models.CharField(max_length=300)
    costoBebida = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def getNombreBebida(self):
        return self.nombreBebida

    def getCostoBebida(self):
        return self.costoBebida
        
    def __str__(self):
        return self.nombreBebida + " | " + str(self.costoBebida)

#######################################################################

# Tabla pedido para almacenar la fecha del pedido y quien lo hizo (Cliente)
#######################################################################
class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fechaPedido = models.DateField('Fecha pedido')
    nombreCliente = models.CharField(max_length=300)

    def sandwiches(self):
        return self.sandwich_set.all()

    def bebidas(self):
        return self.bebidas_set.all()

    def costoTotal(self):

        contS = 0
        contB = 0

        for totS in self.sandwich_set.all():
            contS = contS + totS.costoSandwich()
        
        for totB in self.bebidas_set.all():
            contB = contB + totB.getCostoBebida()

        cantidadTotal = contS + contB

        return cantidadTotal

    def __str__(self):
        return self.nombreCliente
    
    def cantidad_sandwiches(self):
        return len(self.sandwich_set.all())

    def cantidad_bebidas(self):
        return len(self.bebidas_set.all())

#######################################################################

# Tabla sandwich para almacenar el pedido y el tamaño
#######################################################################
class Sandwich(models.Model):
    id_sandwich = models.AutoField(primary_key=True)
    fk_pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING)
    fk_tamano = models.ForeignKey(Tamano, on_delete=models.DO_NOTHING)
    
    def ingredientes(self):
        return self.sandwich_ingrediente_set.all()

    def cantidad_ingredientes(self):
        return len(self.sandwich_ingrediente_set.all())

    def costoSandwich(self):
        cont = 0
        for ing in self.sandwich_ingrediente_set.all().filter()[0:]:
            cont = cont + ing.id_ingrediente.getCostoIngrediente()
        return cont + self.id_tamano.getCostoTamano()

#######################################################################

# Tabla sandwich_ingrediente para almacenar los ingredientes que tendra el sandwich
#######################################################################
class Sandwich_Ingrediente(models.Model):
    id_sandwich_ingrediente = models.AutoField(primary_key=True)
    fk_sandwich = models.ForeignKey(Sandwich, on_delete=models.DO_NOTHING, default=1)
    fk_ingrediente = models.ForeignKey(Ingrediente, on_delete=models.DO_NOTHING, default=1)

#######################################################################

# Tabla bebida_sandwich para las bebida o bebidas que acompañara el sandwich
#######################################################################
class Bebida_Sandwich(models.Model):
    id_bebida_sandwich = models.AutoField(primary_key=True)
    fk_sandwich = models.ForeignKey(Sandwich, on_delete=models.DO_NOTHING, default=1)
    fk_bebida = models.ForeignKey(Bebida, on_delete=models.DO_NOTHING, default=1)

 #######################################################################   
