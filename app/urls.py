from django.urls import path, include
from .views import *
from rest_framework import routers

# GENERAMOS TODAS LAS RUTAS DEL CRUD PRODUCTO
# URL : api/producto

router = routers.DefaultRouter()
router.register('productos', ProductoViewSet)


urlpatterns = [
    path('', index, name="index"),
    path('productos', productos, name="productos"),
    path('contacto', contacto, name="contacto"),
    path('agregar-productos/', agregar_productos, name="agregar_productos"),
    path('modificar-productos/<id>/', modificar_productos, name="modificar_productos"),
    path('eliminar-productos/<id>/', eliminar_productos, name="eliminar_productos"),
    path('login/', login, name="login"),
    path('registro-usuario/', registro_usuario, name="registro_usuario"),
    path('api/', include(router.urls)),
]
