from.models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class formularioRegistro(UserCreationForm):
    class Meta:
        model= User
        fields = ['username','first_name','last_name','email','password1','password2']

class formularioSolicitudServ(ModelForm):
    fecha_servicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    usuario = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model = Solicitud_Servicio
        fields =['usuario','Producto','Descripcion', 'fecha_servicio']
        