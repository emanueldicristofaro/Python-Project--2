from django.contrib import admin
from .models import Bebida_Sandwich, Sandwich_Ingrediente, Tamano, Pedido, Bebida, Ingrediente, Sandwich

# Register your models here.
admin.site.register(Pedido)
admin.site.register(Tamano)
admin.site.register(Bebida)
admin.site.register(Ingrediente)
admin.site.register(Sandwich)
admin.site.register(Sandwich_Ingrediente)
admin.site.register(Bebida_Sandwich)
