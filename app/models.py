from django.db import models

# Create your models here.
class TipoProducto(models.Model):
    tipo = models.CharField(max_length=40)

    def __str__(self):
        return self.tipo

class Producto(models.Model):
    nombre = models.CharField(max_length=40)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoProducto,on_delete=models.CASCADE)
    fecha = models.DateField()
    imagen = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre

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
        



# python manage.py makemigrations -- CREA EL ARCHIVO DE MIGRACION PARA LA BD
# python manage.py migrate -- ENVIA EL ARCHIVO A LA BD
# python manage.py createsuperuser -- CREA EL ADMIN DE LA WEB
# pip install pillow -- NOS PERMITE TRABAJAR CON LAS IMAGENES EN DJANGO