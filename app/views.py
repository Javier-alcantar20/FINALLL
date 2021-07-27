from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core import paginator
from app.forms import ProductoForm, UsuarioCreationForm
from app.models import Producto
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets
from .serializers import ProductoSerializer
# Create your views here.

def index(request):
    return render(request, 'app/index.html')
@permission_required('app.view_producto')
def productos(request):
    productosAll = Producto.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productosAll, 5)
        productosAll = paginator.page(page)
    except: 
        raise Http404
    datos = {
        'listasProductos' : productosAll,
        'paginator' : paginator
    }
    return render(request, 'app/productos.html', datos)

def contacto(request):
    return render(request, 'app/contacto.html')
@permission_required('app.add_producto')
def agregar_productos(request):
    datos = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = 'Producto guardado correctamente'

        datos['form'] = formulario
    return render(request, 'app/agregar_productos.html', datos)

@permission_required('app.change_producto')
def modificar_productos(request, id):
    producto = Producto.objects.get(id=id)
    datos = {
        'form': ProductoForm(instance=producto)
    }


    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = 'Producto modificado correctamente'
            datos['form'] = formulario

    return render(request, 'app/modificar_productos.html', datos)
@permission_required('app.delete_producto')
def eliminar_productos(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()

    return redirect(to="productos")

def login(request):
    return render(request, 'registration/login.html')
    
def registro_usuario(request):

    datos =  {
        'form' : UsuarioCreationForm()
    }

    if request.method == 'POST':
        formulario = UsuarioCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect(to="index")
        datos['form'] = formulario

    return render(request, 'registration/signup.html', datos)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer