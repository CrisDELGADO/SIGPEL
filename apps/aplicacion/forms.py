# -*- coding: utf-8
from django import forms
from django.forms import ModelForm
from .models import *

'''
class UsuarioForm(ModelForm):
    usu_nombre = forms.CharField(label='Nombre:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Nombres','required':'','onKeyPress':'return sololetras(event)'}))
    usu_apellido = forms.CharField(label='Apellido',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Apellidos','required':'','onKeyPress':'return sololetras(event)'}))
    usu_email = forms.EmailField(label='Correo:',max_length=150,widget=forms.TextInput(attrs={'placeholder':'Correo Electrónico','required':'','type':'email'}))
    usu_codigo = forms.CharField(label='Cédula:',max_length=10,widget=forms.TextInput(attrs={'placeholder':'Cédula de Identidad','required':'','onKeyPress':'return solonumeros(event)'}))
    usu_telefono = forms.CharField(label='Teléfono:',max_length=10,widget=forms.TextInput(attrs={'placeholder':'Teléfono fijo o móvil','required':'','onKeyPress':'return solonumeros(event)'}))
    usu_fecha_nac = forms.DateField(label='Nacimiento:',widget=forms.TextInput(attrs={'type':'date','required':''}))
    usu_contrasena = forms.CharField(label='Contraseña:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Contraseña','required':'','type':'password'}))
    contrasena2 = forms.CharField(label='Confirmar Contraseña:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Confirmar Contraseña','required':'','type':'password'}))
    varProvincia = Provincia.objects.all()
    listaProvincias = {(0,0)}
    for x in varProvincia:
        listaProvincias.add((x.prov_codigo,x.prov_nombre))
    listaProvincias.remove((0,0))
    provincia = forms.ChoiceField(choices=listaProvincias)

    class Meta:
        #model = Usuario

        fields = ['usu_nombre','usu_apellido','usu_email','usu_codigo','usu_telefono','usu_fecha_nac','ciu_codigo','rol_codigo','usu_contrasena','contrasena2','provincia']

'''

class UsuarioLogin(forms.Form):
    username = forms.EmailField(label='Correo:',max_length=150,widget=forms.TextInput(attrs={'placeholder':'Correo Electrónico','required':'','type':'email'}))
    password = forms.CharField(label='Contraseña:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Contraseña','required':'','type':'password'}))

    class Meta:
        fields = ['username','password']


class UserRegistro_Form(ModelForm,forms.Form):
    nombres = forms.CharField(label='Nombre:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Nombres','required':'','onKeyPress':'return sololetras(event)'}))
    apellidos = forms.CharField(label='Apellido:',max_length=50,widget=forms.TextInput(attrs={'placeholder':'Apellidos','required':'','onKeyPress':'return sololetras(event)'}))
    username = forms.EmailField(label='Correo:',max_length=150,widget=forms.TextInput(attrs={'placeholder':'Correo Electrónico','required':'','type':'email'}))
    cedula = forms.CharField(label='Cédula:',max_length=10, min_length=10,widget=forms.TextInput(attrs={'placeholder':'Cédula de Identidad','required':'','onKeyPress':'return solonumeros(event)'}))
    telefono = forms.CharField(label='Teléfono:',max_length=10,min_length=7,widget=forms.TextInput(attrs={'placeholder':'Teléfono fijo o móvil','required':'','onKeyPress':'return solonumeros(event)'}))
    password = forms.CharField(label='Contraseña:',max_length=20,min_length=6,widget=forms.TextInput(attrs={'placeholder':'Contraseña','required':'','type':'password'}))
    password2 = forms.CharField(label='Confirmar Contraseña:',max_length=20,min_length=6,widget=forms.TextInput(attrs={'placeholder':'Confirmar Contraseña','required':'','type':'password'}))
    fecha_nac = forms.DateField(label='Nacimiento:',widget=forms.TextInput(attrs={'type':'date','required':''}))
    provincia = forms.CharField(label='Provincia:',required=False,widget=forms.TextInput(attrs={'placeholder':'Provincia','disabled':''}))
    clave = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Clave-Rol','required':'','type':'password'}))

    '''
    varProvincia = Provincia.objects.all()
    listaProvincias = {(0,0)}
    varPrimera = ''
    for x in varProvincia:
        listaProvincias.add((x.id,x.nombre))
        varPrimera = x.id
    listaProvincias.remove((0,0))
    provincia = forms.ChoiceField(choices=listaProvincias)


    varCiudad = Ciudad.objects.filter(provincia_id=varPrimera)
    listaCiudades = {(0,0)}
    for x in varCiudad:
        listaCiudades.add((x.id,x.nombre))
    listaCiudades.remove((0,0))
    ciudad = forms.ChoiceField(choices=listaCiudades)
    '''

    class Meta:
        model = User
        fields = ['nombres','apellidos','cedula','username','fecha_nac','telefono','password','password2','ciudad','provincia','rol','clave']


    def clean_cedula(self):
        varCedula = self.cleaned_data.get('cedula')
        if not validadorDeCedula(varCedula):
            raise forms.ValidationError('Cédula no válida')
        return self.cleaned_data.get('cedula')

    def clean_password2(self):
        varPassword = self.cleaned_data.get('password')
        varPassword2 = self.cleaned_data.get('password2')

        if not varPassword == varPassword2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return self.cleaned_data.get('password2')

    def clean_clave(self):
        varRol = self.cleaned_data.get('rol')
        varClave = self.cleaned_data.get('clave')

        print varRol
        print varClave

        verRol = Rol.objects.get(nombre=varRol)
        if not varClave == verRol.clave:
            raise forms.ValidationError('Clave incorrecta para rol')
        return self.cleaned_data.get('clave')


def validadorDeCedula(cedula):
    cedulaCorrecta = False
    numProvincias = 24
    coeficientes = {2,1,2,1,2,1,2,1,2}
    total = 0

    if (len(cedula) == 10):

        dosDigitos = cedula[0:2]
        tercerDigito = cedula[2]
        print dosDigitos
        print tercerDigito

        if int(dosDigitos) > 0 and int(dosDigitos) <= numProvincias and int(tercerDigito) < 6:
            verificador = int(cedula[9])
            print verificador
            i = 0
            while i<9:
                valor1 = int(cedula[i])
                print valor1
                if i % 2 == 0 or i == 0:
                    valor2 = 2
                else:
                    valor2 = 1
                valor = valor1*valor2
                if valor >= 10:
                    valor = valor - 9
                total += valor
                i+=1

            total2 = total.__str__()
            op = (int(total2[0])+1)*10
            res = op - total

            if res == 10:
                res = 0

            if res == verificador:
                cedulaCorrecta = True
            else:
                cedulaCorrecta = False

        else:
            cedulaCorrecta = False
    else:
        cedulaCorrecta = False

    return cedulaCorrecta



class Categoria_Form(ModelForm):
    nombre = forms.CharField(label='Nombre:',max_length=30,widget=forms.TextInput(attrs={'placeholder':'Nombre','required':''}))
    descripcion = forms.CharField(label='Descripción:',max_length=100,widget=forms.TextInput(attrs={'placeholder':'Descripción','required':''}))


    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']


class Producto_Form(ModelForm):
    nombre = forms.CharField(label='Nombre:',max_length=30,widget=forms.TextInput(attrs={'placeholder':'Nombre','required':'','onKeyPress':'return sololetras(event)'}))
    descripcion = forms.CharField(label='Descripción:',max_length=100,widget=forms.TextInput(attrs={'placeholder':'Descripción','required':''}))
    precio = forms.CharField(label='Precio:',max_length=100,widget=forms.TextInput(attrs={'placeholder':'Precio','required':'','onKeyPress':'return solonumerosdecimales(event)'}))
    cantidad = forms.IntegerField()
    imagen1 = forms.ImageField(label='Imagen #1', required=False)
    imagen2 = forms.ImageField(label='Imagen #2', required=False)
    imagen3 = forms.ImageField(label='Imagen #3', required=False)
    imagen4 = forms.ImageField(label='Imagen #4', required=False)
    imagen5 = forms.ImageField(label='Imagen #5', required=False)

    class Meta:
        model = Producto
        fields = ['nombre','descripcion','precio','cantidad','categoria','imagen1','imagen2','imagen3','imagen4','imagen5']


class Foto_Form(ModelForm):

    class Meta:
        model = Foto
        fields = ['imagen','producto']


class Pedido_Form(ModelForm):
    fecha_ini = forms.DateField(label='Inicio:',widget=forms.TextInput(attrs={'type':'date','required':''}))
    fecha_fin = forms.DateField(label='Fin:',widget=forms.TextInput(attrs={'type':'date','required':''}))

    class Meta:
        model = Pedido
        fields = ['fecha_ini','fecha_fin','estado','usuario']