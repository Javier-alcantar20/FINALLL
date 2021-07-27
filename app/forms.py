from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .validators import TamañoMaximoValidator



class ProductoForm(ModelForm):
    nombre= forms.CharField(min_length=5, max_length=20)
    precio = forms.IntegerField(min_value=9000)
    imagen = forms.ImageField(validators=[TamañoMaximoValidator(1)], required=False)
    
    def clean_nombre(self):
        nom = self.cleaned_data["nombre"]
        aux = Producto.objects.filter(nombre__iexact=nom).exists()

        if aux:
            raise ValidationError("Este producto ya existe.")
        return nom

    class Meta:
        model = Producto
        fields = '__all__'
        #fields = ['nombre','precio','descripcion', 'tipo', 'fecha', 'imagen']

        widgets = {
            'fecha': forms.SelectDateWidget(years=range(2018,2022))
        }

class UsuarioCreationForm(UserCreationForm):
    
    class Meta: 
        model = User
        #fields = '__all__'
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
