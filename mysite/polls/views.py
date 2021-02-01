from django.shortcuts import render
from .models import Tamano, Ingrediente

def index(request):
    tamanos = Tamano.objects.all()
    ingredientes = Ingrediente.objects.all()
    contex = {'tamanos' : tamanos, 'ingredientes' : ingredientes}
    return render(request, 'pedidos/index.html', contex)