from rest_framework import serializers
from .models import Producto, TipoProducto, Cart
from django.forms import ValidationError

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'



class ProductoSerializer(serializers.ModelSerializer):
    tipo = TipoProductoSerializer(read_only=True)
    tipo_producto = serializers.PrimaryKeyRelatedField(queryset=TipoProducto.objects.all(), source="tipo")

    class Meta:
        model = Producto
        fields = '__all__'

    def validate_nombre(self, value):
        aux = Producto.objects.filter(nombre__iexact=value).exists()

        if aux:
            raise ValidationError("Este producto ya existe.")
        return value

    
    def validate_precio(self, value):
        if value< 9000:
            raise ValidationError("El precio no puede ser menor a 9000.")
        return value

class Cart:
        def __init__(self, request):
            self.request = request
            self.session = request.session

            cart = self.session.get("cart")
            if not cart:
                cart = self.session["cart"] = {}

            else:
                self.cart = cart
        
        def add(self, producto):
            if str(producto.id) not in self.cart.keys():
                self.cart[producto.id] = {
                    "producto_id": producto.id,
                    "nombre" : producto.id,
                    "cantidad": 1,
                    "precio": str(producto.precio),
                    "image" : producto.image.url
                }
            else:
                for key, value in self.cart.items():
                    if key == str(producto.id):
                        value["cantidad"] = value["cantidad"] + 1

                   
                    break

            self.save()

        def save(self):
            self.session["cart"] = self.cart
            self.session.modified = True
        
        def remove(self, producto):
            producto.id = str(producto.id)
            if producto.id in self.cart:
                del self.cart[producto.id]
                self.save()
        
        def decrement(self, producto):
            for key, value in self.cart.items():
                if key == str(producto.id):
                    value["cantidad"] = value["cantidad"] - 1
                    
                    if value["cantidad"] <1:
                        self.remove(producto)
                    
                    else:
                        self.save()
                    break
                else:
                    print("El producto no existe en el carrito")
        
        def clear(self):
            self.session["cart"] ={}
            self.session.modified = True
        
            