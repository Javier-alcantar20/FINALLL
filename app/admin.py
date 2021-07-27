from app.forms import ProductoForm
from app.models import Producto, TipoProducto
from django.contrib import admin

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio', 'descripcion', 'tipo']
    search_fields = ['nombre']
    list_per_page = 5
    form = ProductoForm


admin.site.register(TipoProducto)
admin.site.register(Producto, ProductoAdmin)
