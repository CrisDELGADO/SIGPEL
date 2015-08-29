# -*- coding: utf-8
import json
import datetime


from django.shortcuts import render, render_to_response
from django.http import request, HttpResponse, HttpResponseRedirect, Http404
from django.template import context, RequestContext
from django.views.generic import TemplateView, FormView, CreateView, UpdateView
import time
from reportlab.graphics.renderPDF import drawToString
from reportlab.platypus.para import Para
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.db.models import Q

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


'''
class IndexView(TemplateView):
    form_class = UserRegistro_Form
    template_name = 'aplicacion/index.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(IndexView,self).form_valid(form)
'''


def vista_inicio(request):
    if request.method == 'POST':
        if 'botonLogeo' in request.POST:
            formLogin = UsuarioLogin(request.POST)

            if formLogin.is_valid():
                print 'Logeo validado'

                user = authenticate(username=formLogin.cleaned_data['username'],password=formLogin.cleaned_data['password'])

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/')
                else:
                    print 'Usuario o contraseña incorrectos'

    else:
        formLogin = UsuarioLogin()

    return render(request, 'base.html', {'formularioLogeo': formLogin}, context_instance=RequestContext(request))


class vista_login(TemplateView):
     def get(self, request, *args, **kwargs):
        if request.is_ajax():

            nombreUser = request.GET['usuario']
            passUser = request.GET['password']


            formLogin = UsuarioLogin(nombreUser, passUser)

            print nombreUser


            datos=[]
            resul = {}

            if nombreUser=='' or passUser=='':
                resul['errorUsername']='Ambos campos son obligatorios'
                datos.append(resul)
            else:
                user = authenticate(username=nombreUser,password=passUser)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        resul['errorUsername']='yes'
                        datos.append(resul)
                        #return HttpResponseRedirect('/')
                else:
                    resul['errorUsername']='Usuario o Contraseña incorrectos'
                    datos.append(resul)



            data = json.dumps(datos)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404

class vista_misDatos_ajax(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            nombres=request.GET['nombres']
            apellidos=request.GET['apellidos']
            fecha_nac=request.GET['fecha_nac']
            ciudad=request.GET['ciudad']
            telefono=request.GET['telefono']
            username=request.GET['username']

            editUser = User.object.get(id=request.user.id)
            res={}
            res['co']=False

            if not editUser.username == username:
                try:
                    verCorreo = User.object.get(username=username)
                    print verCorreo

                    if verCorreo:
                        res['co']=True


                except:
                    print 'No hay'
                    editUser.username = username
                    editUser.save()
                    res['co']=False


            editUser.nombres = nombres
            editUser.apellidos = apellidos
            editUser.telefono = telefono
            editUser.fecha_nac = fecha_nac
            editUser.ciudad_id = ciudad

            print nombres, apellidos, fecha_nac, ciudad, telefono

            editUser.save()


            res['respuesta']='Cambios Guardados'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404


class vista_misDatos_contra_ajax(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            contraAc=request.GET['contraAc']
            contraNu=request.GET['contraNu']
            contraCo=request.GET['contraCo']

            editUser = User.object.get(id=request.user.id)

            res={}

            if editUser.check_password(contraAc):
                if contraNu == contraCo:
                    editUser.set_password(contraNu)
                    editUser.save()

                    res['respuesta']='Contraseña Cambiada'
                    res['valido']=True
                else:
                    res['respuesta']='Contraseñas nuevas no coinciden!'
                    res['valido']=False
            else:
                res['respuesta']='Contraseña Actual incorrecta!!'
                res['valido']=False



            #editUser.save()




            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404


def vista_misDatos(request):
    editUser = request.user

    datoCiudad = Ciudad.objects.get(id=editUser.ciudad_id)
    datoProvincia = Provincia.objects.get(id=datoCiudad.provincia_id)
    print datoProvincia.nombre



    if request.method == 'POST':
        formActualizar = UserRegistro_Form(request.POST)

        if 'botonActualizar' in request.POST:
            print formActualizar['cedula']
            formActualizar.username = 'xxxxxx@xxx.xxx'
            formActualizar.cedula = '1111111111'
            print formActualizar
            if formActualizar.is_valid():
                print 'Validado actualizar'

                #username=formActualizar.cleaned_data['username']
                #password=formActualizar.cleaned_data['password']
                nombres=formActualizar.cleaned_data['nombres']
                apellidos=formActualizar.cleaned_data['apellidos']
                #cedula=formActualizar.cleaned_data['cedula']
                fecha_nac=formActualizar.cleaned_data['fecha_nac'],
                ciudad=formActualizar.cleaned_data['ciudad']
                telefono = formActualizar.cleaned_data['telefono']
                #rol=formActualizar.cleaned_data['rol']

                #editUser = User.object.get(id=editUser.id)

                editUser.nombres = nombres
                editUser.apellidos = apellidos
                editUser.telefono = telefono
                editUser.fecha_nac = fecha_nac
                editUser.ciudad = ciudad
                '''
                editUser.apellidos = apellidos
                editUser.fecha_nac = fecha_nac
                editUser.ciudad = ciudad
                editUser.password = password
                '''

                editUser.save()

                return HttpResponseRedirect('/misdatos')
    else:
        formActualizar = UserRegistro_Form(instance=editUser)

    ctx = {
        'formActualizar':formActualizar,
        'nombreProvincia':datoProvincia.nombre

    }

    return render(request,'aplicacion/misDatos.html', ctx, context_instance=RequestContext(request))


def vista_usuario(request):
    if request.method == 'POST':
        form = UserRegistro_Form(request.POST)

        if form.is_valid():
            User.object.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password'],
                                    nombres=form.cleaned_data['nombres'],apellidos=form.cleaned_data['apellidos'],
                                    cedula=form.cleaned_data['cedula'],fecha_nac=form.cleaned_data['fecha_nac'],
                                    ciudad=form.cleaned_data['ciudad'],rol=form.cleaned_data['rol'],
                                    telefono=form.cleaned_data['telefono'])
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/')
            return HttpResponseRedirect('/usuario')
    else:
        form = UserRegistro_Form()
    return render(request, 'aplicacion/usuario.html', {'form': form}, context_instance=RequestContext(request))

class vista_usuario2(FormView):
    form_class = UserRegistro_Form
    template_name = 'aplicacion/usuario.html'
    success_url = '/usuario/'

def vista_usuario_ajax(request):
    print 'formLlego'
    if request.is_ajax() and request.method == 'POST':
        form = UserRegistro_Form(request.POST)
        print 'formLlego2'

        errores = ''
        if form.is_valid():
            print 'valido'
            User.object.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password'],
                                    nombres=form.cleaned_data['nombres'],apellidos=form.cleaned_data['apellidos'],
                                    cedula=form.cleaned_data['cedula'],fecha_nac=form.cleaned_data['fecha_nac'],
                                    ciudad=form.cleaned_data['ciudad'],rol=form.cleaned_data['rol'])

            return HttpResponseRedirect('/usuario')
        else:
            print 'no valido'
            errores = form.errors

        response = {}
        response['errores']=errores
        res = []
        res.append(response)



        #data = serializers.serialize('json', response)
        data = json.dumps(res)
        return HttpResponse(data, content_type='application/json')

    else:
        raise Http404

def vista_nuevoUsuario_ajax(request):
    if request.is_ajax():
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        username = request.POST.get('username')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        fecha_nac = request.POST.get('fecha_nac')
        ciudad = request.POST.get('ciudad')
        rol = request.POST.get('rol')
        clave = request.POST.get('clave')



        '''
        formUsuario = UserRegistro_Form(nombres=nombres, apellidos=apellidos, username=username, cedula=cedula, telefono=telefono,
                                        password=password, fecha_nac=fecha_nac, ciudad=ciudad, rol=rol)
        '''

        respuesta = {}



        verUsername = User.objects.get(Q(username=username))
        if verUsername:
            respuesta['ErrorUsername']='Ya hay un usuario con este correo'
        else:
            print 'no hay'

        verCedula = User.objects.get(Q(cedula=cedula))
        if verCedula:
            respuesta['ErrorCedula']='Ya hay un usuario con esta cédula'

        if len(cedula)<10:
            respuesta['ErrorCedula']='Debe tener 10 números'


        data = json.dumps(respuesta)

        print data

        return HttpResponse(data, content_type='application/json')
    else:
        print 'Los jodi'

class vista_provincia(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():

            id_ciudad = request.GET['ciudad_id']
            ciudadEs = Ciudad.objects.get(id=id_ciudad)

            provinciaSe = Provincia.objects.get(id=ciudadEs.provincia_id)


            res = {}
            res['id']=provinciaSe.id
            res['nombre']=provinciaSe.nombre

            data = json.dumps(res)
            print data
            return HttpResponse(data, content_type='application/json')
        else:
            return Http404

def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect('/')



def vista_informacion(request):
    return render(request, 'aplicacion/informacion.html', context_instance=RequestContext(request))

class vista_verificar_fecha(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax:
            fechaSistema = datetime.date.today()
            verPedidos = Pedido.objects.filter(estado='PENDIENTE')
            for ped in verPedidos:
                if ped.fecha_fin < fechaSistema:
                    ped.estado = 'ANULADO'
                    ped.save()


            res = {}
            res['respuesta']='EMELEC'

            data = json.dumps(res)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404

def vista_administrar(request):
    if request.method == 'POST':

        if 'botonAgregarCategoria' in request.POST:
            formCategoria = Categoria_Form(request.POST)
            if formCategoria.is_valid():
                formCategoria.save()

        if 'botonAgregarProducto' in request.POST:
            print 'accionnnnnnnn'
            formProducto = Producto_Form(request.POST, request.FILES)



            if formProducto.is_valid():
                nombre=formProducto.cleaned_data['nombre']
                print nombre
                descripcion=formProducto.cleaned_data['descripcion']
                precio=formProducto.cleaned_data['precio']
                cantidad=formProducto.cleaned_data['cantidad']
                categoria=formProducto.cleaned_data['categoria']
                imagen1=formProducto.cleaned_data['imagen1']
                imagen2=formProducto.cleaned_data['imagen2']
                imagen3=formProducto.cleaned_data['imagen3']
                imagen4=formProducto.cleaned_data['imagen4']
                imagen5=formProducto.cleaned_data['imagen5']
                nuevoProducto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, categoria=categoria)
                nuevoProducto.save()
                if imagen1:
                    nuevoFotoProducto1 = Foto(imagen=imagen1, producto_id=nuevoProducto.id)
                    nuevoFotoProducto1.save()
                if imagen2:
                    nuevoFotoProducto2 = Foto(imagen=imagen2, producto_id=nuevoProducto.id)
                    nuevoFotoProducto2.save()
                if imagen3:
                    nuevoFotoProducto3 = Foto(imagen=imagen3, producto_id=nuevoProducto.id)
                    nuevoFotoProducto3.save()
                if imagen4:
                    nuevoFotoProducto4 = Foto(imagen=imagen4, producto_id=nuevoProducto.id)
                    nuevoFotoProducto4.save()
                if imagen5:
                    nuevoFotoProducto5 = Foto(imagen=imagen5, producto_id=nuevoProducto.id)
                    nuevoFotoProducto5.save()
                if not imagen1 and not imagen2 and not imagen3 and not imagen2 and not imagen1:
                    nuevoFotoProductoDefault = Foto(imagen='default.png', producto_id=nuevoProducto.id)
                    nuevoFotoProductoDefault.save()

                return HttpResponseRedirect('/administrar-producto/#contenidoPrincipal')


        if 'botonAgregarImagenProducto' in request.POST:
            formFoto =  Foto_Form(request.POST, request.FILES)
            print 'llego'
            if formFoto.is_valid():
                print 'foto validado'
                formFoto.save()
                return HttpResponseRedirect('/')


    else:
        formCategoria = Categoria_Form()
        formProducto = Producto_Form()
        formFoto = Foto_Form()



    ctx ={
        'formProducto':formProducto,
        #'formFoto':formFoto,
    }
    return render(request, 'aplicacion/administrar.html',ctx, context_instance=RequestContext(request))

def vista_administrar_categoria(request):
    formCategoria = Categoria_Form
    listaCategoriasAdmin = Categoria.objects.all()
    ctx = {
        'formCategoria':formCategoria,
        'listaCategoriasAdmin':listaCategoriasAdmin
    }
    return render(request, 'aplicacion/administrar-categoria.html',ctx, context_instance=RequestContext(request))

class vista_administrar_categoria_agregar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            nombre = request.GET['nombre']
            descripcion = request.GET['descripcion']

            nuevaCategoria = Categoria(nombre=nombre, descripcion=descripcion)
            nuevaCategoria.save()

            res = {}
            res['respuesta']='Categoría Agregada'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404

class vista_administrar_categoria_editar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cat_id = request.GET['cat_id']
            nombre = request.GET['nombre']
            descripcion = request.GET['descripcion']

            editarCategoria = Categoria.objects.get(id=cat_id)
            editarCategoria.nombre = nombre
            editarCategoria.descripcion = descripcion
            editarCategoria.save()

            res = {}
            res['respuesta']='Cambios Guardados'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404


class vista_administrar_categoria_eliminar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cat_id = request.GET['cat_id']

            eliminarCategoria = Categoria.objects.get(id=cat_id)
            res = {}
            try:
                eliminarCategoria.delete()
                res['respuesta']='Categoría Eliminada'
            except:
                res['respuesta']='No se pudo eliminar esta categoría'



            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404


class vista_listaCategorias_admin(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            categoria_cod = request.GET['cat_id']
            categoria = Categoria.objects.get(id=categoria_cod)

            res = {}
            res['nombre']=categoria.nombre
            res['descripcion']=categoria.descripcion


            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')
        else:
            raise  Http404

class vista_listaProductos_admin(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            producto_cod = request.GET['pro_id']
            print producto_cod
            producto = Producto.objects.get(id=producto_cod)

            res = {}
            res['nombre2']=producto.nombre
            res['descripcion2']=producto.descripcion
            res['precio2']=producto.precio
            res['cantidad2']=producto.cantidad
            res['categoria2']=producto.categoria_id

            res['imagen12']=''
            res['imagen22']=''
            res['imagen32']=''
            res['imagen42']=''
            res['imagen52']=''

            listaFoto = Foto.objects.filter(producto_id=producto_cod)
            print listaFoto
            cont = 1
            for ima in listaFoto:
                if cont==1:
                    res['imagen12']=ima.imagen.__str__()
                if cont==2:
                    res['imagen22']=ima.imagen.__str__()
                if cont==3:
                    res['imagen32']=ima.imagen.__str__()
                if cont==4:
                    res['imagen42']=ima.imagen.__str__()
                if cont==5:
                    res['imagen52']=ima.imagen.__str__()
                cont += 1



            data = json.dumps(res)

            print data

            return HttpResponse(data, content_type='application/json')
        else:
            raise  Http404

def vista_administrar_producto(request):

    if request.method=='POST':
        formProducto = Producto_Form(request.POST, request.FILES)

        if formProducto.is_valid():
            nombre=formProducto.cleaned_data['nombre']
            descripcion=formProducto.cleaned_data['descripcion']
            precio=formProducto.cleaned_data['precio']
            cantidad=formProducto.cleaned_data['cantidad']
            categoria=formProducto.cleaned_data['categoria']
            imagen1=formProducto.cleaned_data['imagen1']
            imagen2=formProducto.cleaned_data['imagen2']
            imagen3=formProducto.cleaned_data['imagen3']
            imagen4=formProducto.cleaned_data['imagen4']
            imagen5=formProducto.cleaned_data['imagen5']
            nuevoProducto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, categoria=categoria)
            nuevoProducto.save()
            if imagen1:
                nuevoFotoProducto1 = Foto(imagen=imagen1, producto_id=nuevoProducto.id)
                nuevoFotoProducto1.save()
            if imagen2:
                nuevoFotoProducto2 = Foto(imagen=imagen2, producto_id=nuevoProducto.id)
                nuevoFotoProducto2.save()
            if imagen3:
                nuevoFotoProducto3 = Foto(imagen=imagen3, producto_id=nuevoProducto.id)
                nuevoFotoProducto3.save()
            if imagen4:
                nuevoFotoProducto4 = Foto(imagen=imagen4, producto_id=nuevoProducto.id)
                nuevoFotoProducto4.save()
            if imagen5:
                nuevoFotoProducto5 = Foto(imagen=imagen5, producto_id=nuevoProducto.id)
                nuevoFotoProducto5.save()
            if not imagen1 and not imagen2 and not imagen3 and not imagen2 and not imagen1:
                nuevoFotoProductoDefault = Foto(imagen='default.png', producto_id=nuevoProducto.id)
                nuevoFotoProductoDefault.save()

            return HttpResponseRedirect('/administrar-producto/#contenidoPrincipal')

    else:
        formProducto= Producto_Form()
        listaProductos = Producto.objects.all().order_by('id')
        listaCategorias = Categoria.objects.all().order_by('id')

    ctx = {
        'formProducto':formProducto,
        'listaProductosAdmin':listaProductos,
        'listaCategoriasAdmin':listaCategorias
    #    'listaCategoriasAdmin':listaCategoriasAdmin
    }
    return render(request, 'aplicacion/administrar-producto.html',ctx, context_instance=RequestContext(request))

class vista_administrar_producto_agregar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            nombre = request.GET['nombre']
            descripcion = request.GET['descripcion']
            precio=request.GET['precio']
            cantidad=request.GET['cantidad']
            categoria=request.GET['categoria']
            imagen1=request.GET['imagen1']
            imagen2=request.GET['imagen2']
            imagen3=request.GET['imagen3']
            imagen4=request.GET['imagen4']
            imagen5=request.GET['imagen5']

            nuevoProducto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, categoria_id=categoria)
            nuevoProducto.save()

            print 'guardo'

            if imagen1:
                nuevoFotoProducto1 = Foto(imagen=imagen1, producto_id=nuevoProducto.id)
                nuevoFotoProducto1.save()
            if imagen2:
                nuevoFotoProducto2 = Foto(imagen=imagen2, producto_id=nuevoProducto.id)
                nuevoFotoProducto2.save()
            if imagen3:
                nuevoFotoProducto3 = Foto(imagen=imagen3, producto_id=nuevoProducto.id)
                nuevoFotoProducto3.save()
            if imagen4:
                nuevoFotoProducto4 = Foto(imagen=imagen4, producto_id=nuevoProducto.id)
                nuevoFotoProducto4.save()
            if imagen5:
                nuevoFotoProducto5 = Foto(imagen=imagen5, producto_id=nuevoProducto.id)
                nuevoFotoProducto5.save()
            if not imagen1 and not imagen2 and not imagen3 and not imagen2 and not imagen1:
                nuevoFotoProductoDefault = Foto(imagen='default.png', producto_id=nuevoProducto.id)
                nuevoFotoProductoDefault.save()

            res = {}
            res['respuesta']='Producto Agregado'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404

class vista_administrar_producto_editar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            pro_id = request.GET['id']
            nombre = request.GET['nombre']
            descripcion = request.GET['descripcion']
            precio = request.GET['precio']
            cantidad = request.GET['cantidad']
            categoria = request.GET['categoria']



            editProducto = Producto.objects.get(id=pro_id)
            print editProducto.nombre
            print editProducto.descripcion
            print editProducto.precio
            print editProducto.cantidad
            print editProducto.categoria_id

            editProducto.nombre = nombre
            editProducto.descripcion = descripcion
            editProducto.precio = precio
            editProducto.cantidad = cantidad
            editProducto.categoria_id = categoria
            print editProducto
            editProducto.save()

            print 'guardo'

            res = {}
            res['respuesta']='Cambios Guardados'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404

class vista_administrar_producto_eliminar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            pro_id = request.GET['id']

            eliminarProducto = Producto.objects.get(id=pro_id)
            res = {}
            try:
                eliminarProducto.delete()
                res['respuesta']='Producto Eliminado'
            except:
                res['respuesta']='No se pudo eliminar este producto'



            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404

def vista_administrar_usuario(request):

    listaUser = User.object.filter(rol_id=3).order_by('id')

    print listaUser

    ctx = {
        'usuarios':listaUser
    }

    return render(request, 'aplicacion/administrar-usuario.html',ctx , context_instance=RequestContext(request))

class vista_administrar_usuario_estado(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            us_id = request.GET['id']
            us_est = request.GET['est']

            if us_est=='true' or us_est=='True':
                us_est = False
            else:
                us_est = True

            editUser = User.object.get(id=us_id)
            editUser.is_active = us_est
            editUser.save()


            res = {}
            res['respuesta']='Estado Cambiado'



            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404


class vista_administrar_usuario_listaUsuarios(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            rol = request.GET['rol']
            try:
                ced = request.GET['busqueda']
                listaUsuario = []
                listaUser = User.object.filter(rol_id=rol,cedula__startswith=ced).order_by('id')
                for lis in listaUser:
                    res = {}
                    res['id2']=lis.id
                    res['cedula2']=lis.cedula
                    res['nombres2']=lis.nombres
                    res['apellidos2']=lis.apellidos
                    res['is_active2']=lis.is_active
                    listaUsuario.append(res)
            except:
                listaUser = User.object.filter(rol_id=rol).order_by('id')
                listaUsuario = []
                for lis in listaUser:
                    res = {}
                    res['id2']=lis.id
                    res['cedula2']=lis.cedula
                    res['nombres2']=lis.nombres
                    res['apellidos2']=lis.apellidos
                    res['is_active2']=lis.is_active
                    listaUsuario.append(res)


            data = json.dumps(listaUsuario)

            return HttpResponse(data, content_type='application/json')


        else:
            raise Http404


def vista_productos(request):
    categorias = Categoria.objects.all().order_by('id')
    categoriaDefault = []


    for x in categorias:
        categoriaDefault = x
        break

    productosPorCategoria = []

    for x in categorias:
        listaProductos=Producto.objects.filter(categoria_id=x.id).order_by('id')
        listaPro = []
        for produc in listaProductos:
            res = {}
            res['id']=produc.id
            res['nombre']=produc.nombre
            res['descripcion']=produc.descripcion
            res['precio']=produc.precio
            res['cantidad']=produc.cantidad
            res['categoria']=produc.categoria
            listaImagen=Foto.objects.filter(producto_id=produc.id)
            for ima in listaImagen:
                res['imagen']=ima.imagen.__str__()
            listaPro.append(res)
        productosPorCategoria.append(listaPro)
        #productosPorCategoria.append(Producto.objects.filter(categoria_id=x.id))


    ctx = {'categorias':categorias,
           'categoriaDefault':categoriaDefault,
           'productosPorCategoria':productosPorCategoria,
           }
    return render(request, 'aplicacion/productos.html',ctx ,context_instance=RequestContext(request))

class vista_productos_filtrar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            id_categoria = request.GET['idCategoria']
            filtrado = request.GET['filtrado']
            filtrado = int(filtrado)
            productoBuscar = request.GET['productoBuscar']



            if filtrado == 1:
                productos = Producto.objects.filter(categoria_id=id_categoria, nombre__icontains=productoBuscar).order_by('id')
            if filtrado == 2:
                productos = Producto.objects.filter(categoria_id=id_categoria, nombre__icontains=productoBuscar).order_by('-id')
            if filtrado == 3:
                productos = Producto.objects.filter(categoria_id=id_categoria, nombre__icontains=productoBuscar).order_by('-precio')
            if filtrado == 4:
                productos = Producto.objects.filter(categoria_id=id_categoria, nombre__icontains=productoBuscar).order_by('precio')


            listaProductos = []
            for prod in productos:
                res = {}
                res['id']=prod.id
                res['nombre']=prod.nombre
                res['descripcion']=prod.descripcion
                res['precio']=prod.precio
                res['cantidad']=prod.cantidad
                res['categoria']=prod.categoria_id
                listaImagen=Foto.objects.filter(producto_id=prod.id)
                for ima in listaImagen:
                    res['imagen']=ima.imagen.__str__()


                listaProductos.append(res)


            data = json.dumps(listaProductos)

            print data
            return HttpResponse(data, content_type='application/json')
        else:
            return Http404


class vista_productos_ajax(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            print 'emelec'
            id_categoria = request.GET['id']
            print 'emelec'
            productos = Producto.objects.filter(categoria_id=id_categoria).order_by('id')
            print 'emelec'
            listaProductos = []
            for prod in productos:
                res = {}
                res['id']=prod.id
                res['nombre']=prod.nombre
                res['descripcion']=prod.descripcion
                res['precio']=prod.precio
                res['cantidad']=prod.cantidad
                res['categoria']=prod.categoria_id
                listaImagen=Foto.objects.filter(producto_id=prod.id)
                for ima in listaImagen:
                    res['imagen']=ima.imagen.__str__()


                listaProductos.append(res)

            print 'emelec'
            data = json.dumps(listaProductos)
            print 'emelec'
            #data = serializers.serialize('json', productos, fields=('id','nombre','precio'))
            print data
            return HttpResponse(data, content_type='application/json')
        else:
            return Http404

def vista_productos_categoria(request, id_categoria):
    categoria = Categoria.objects.get(id=id_categoria)
    productos = Producto.objects.filter(categoria_id=id_categoria).order_by('id')
    productos2 = []
    for prod in productos:
        listaImagen = Foto.objects.filter(producto_id=prod.id)
        res = {}
        res['id']=prod.id
        res['nombre']=prod.nombre
        res['descripcion']=prod.descripcion
        res['precio']=prod.precio
        res['cantidad']=prod.cantidad
        res['categoria']=prod.categoria_id
        listaImagen=Foto.objects.filter(producto_id=prod.id)
        for ima in listaImagen:
            res['imagen']=ima.imagen.__str__()
        productos2.append(res)

    ctx = {
        'categoriaEs':categoria,
        'productosEs':productos2,
    }
    return render(request, 'aplicacion/productos-categoria.html',ctx  ,context_instance=RequestContext(request))

def vista_producto_detalle(request,id_producto):
    producto = Producto.objects.get(id=id_producto)
    categoria = Categoria.objects.get(id=producto.categoria_id)
    imagenes = Foto.objects.filter(producto_id=producto.id)

    listaProductos = Producto.objects.filter(categoria_id=categoria).order_by('id')

    i=len(listaProductos)
    lim=3
    if i < 3:
        lim=i

    comunProductos = []

    while lim > 0:
        i -= 1
        res = {}
        listaImagen=Foto.objects.filter(producto_id=listaProductos[i].id)
        for ima in listaImagen:
            res['imagen']=ima.imagen.__str__()

        res['id']=listaProductos[i].id
        res['nombre']=listaProductos[i].nombre
        res['categoria']=listaProductos[i].categoria
        res['precio']=listaProductos[i].precio

        comunProductos.append(res)
        lim -= 1

    ctx = {
        'producto':producto,
        'categoria':categoria,
        'imagenes':imagenes,
        'productoscomunes':comunProductos,
    }
    return render(request, 'aplicacion/producto-detalle.html' ,ctx ,context_instance=RequestContext(request))

def vista_mispedidos(request):
    print request.user.id
    pedidos = Pedido.objects.filter(usuario_id=request.user.id).order_by('id')

    ctx = {
        'pedidos':pedidos,
    }
    return render(request, 'aplicacion/mispedidos.html',ctx , context_instance=RequestContext(request))

def vista_gestionarpedidos(request):


    usuarios = User.object.all().order_by('id')
    pedidos = Pedido.objects.all().order_by('id')

    ctx = {
        'usuarios':usuarios,
        'pedidos':pedidos,
    }
    return render(request, 'aplicacion/gestionarpedidos.html',ctx , context_instance=RequestContext(request))

class vista_gestionar_ValidarPedido(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            idPedido = request.GET['idPedido']
            instanciaPedido = Pedido.objects.get(id=idPedido)
            instanciaPedido.estado = 'VALIDADO'
            instanciaPedido.save()

            res = {}
            res['respuesta']='Pedido Validado!!'

            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404

class vista_gestionar_VerPedidos(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cedula = request.GET['ced']
            print cedula

            datos={}

            datosFinales = []

            if validadorDeCedula(cedula):
                try:
                    verCedula = User.object.get(cedula=cedula)
                    listaUsuarios = User.object.all()
                    print 'Usuario existe'
                    verPedidos = Pedido.objects.filter(usuario_id=verCedula.id).order_by('-id')
                    if verPedidos:
                        print 'Mostrar pedidos'

                        for verUsu in listaUsuarios:
                            res = {}
                            res['respuesta']='bien'
                            res['usuario_referencia']=verUsu.id
                            res['usuario_id']=verCedula.id
                            datosFinales.append(res)

                    else:
                        datos['respuesta'] = 'No hay pedidos'
                        datosFinales.append(datos)
                except:
                    datos['respuesta'] = 'No existe usuario con esta cédula'
                    datosFinales.append(datos)

            else:
                datos['respuesta'] = 'Número de cédula no válido'
                datosFinales.append(datos)



            data = json.dumps(datosFinales)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404


class vista_pedidoDetalle(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            id_pedido = request.GET['id']
            listapedido = PedidoProducto.objects.filter(pedido_id=id_pedido).order_by('id')
            print listapedido

            datosTabla = []
            sub = 0

            for a in listapedido:
                productos = Producto.objects.get(id=a.producto_id)
                '''
                cant = a.cantidad
                prec = productos.precio
                prec2 = cant * prec2
                '''

                resul = {}
                resul['id']=productos.id
                resul['stock']=productos.cantidad
                resul['cantidad']=a.cantidad
                resul['producto']=productos.nombre
                resul['precio']=productos.precio
                resul['precio']="%.2f" % (resul['precio'])
                resul['precio2']=float(productos.precio)*float(a.cantidad)
                resul['precio2']="%.2f" % (resul['precio2'],)
                sub += float(resul['precio2'])
                resul['sub']="%.2f" % (sub,)
                resul['iva']="%.2f" % (sub*0.12)
                total=float(resul['sub'])+float(resul['iva'])
                resul['total']="%.2f" % (total)


                datosTabla.append(resul)

            data = json.dumps(datosTabla)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404


class vista_pedidoDetalleCancelar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            id_pedido = request.GET['idPedido']

            verListaPedido = PedidoProducto.objects.filter(pedido_id=id_pedido).order_by('id')
            for listadoPedido in verListaPedido:
                cantDevolver = listadoPedido.cantidad
                producto = listadoPedido.producto_id

                instanciaProducto = Producto.objects.get(id=producto)
                cantAc = instanciaProducto.cantidad
                instanciaProducto.cantidad = int(cantAc) + int(cantDevolver)
                instanciaProducto.save()


            instanciaPedido = Pedido.objects.get(id=id_pedido)
            instanciaPedido.delete()


            res = {}
            res['respuesta']='Pedido cancelado'
            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')

        else:
            raise Http404

class vista_pedidoDetalleEditar(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            id_pedido = request.GET['idPedido']
            contador = request.GET['contador']
            contador = int(contador)

            i=0

            listaProductosPedido = PedidoProducto.objects.filter(pedido_id=id_pedido).order_by("id")


            while i<contador:
                cant = request.GET['listaCantidad['+i.__str__()+']']
                borrar = request.GET['listaBorrar['+i.__str__()+']']

                cod_pro = listaProductosPedido[i].producto_id
                cant = int(cant)
                cantB = listaProductosPedido[i].cantidad
                cantB = int(cantB)

                if borrar == 'si':
                    print 'si'
                    nuevaInstanciaPedidoProducto2 = PedidoProducto.objects.get(id=listaProductosPedido[i].id)
                    nuevaInstanciaPedidoProducto2.cantidad = 0
                    nuevaInstanciaPedidoProducto2.save()


                else:
                    print 'no'
                    nuevaInstanciaPedidoProducto = PedidoProducto.objects.get(id=listaProductosPedido[i].id)
                    nuevaInstanciaPedidoProducto.cantidad = cant.__str__()
                    nuevaInstanciaPedidoProducto.save()

                    if cant<cantB:
                        devolver = cantB - cant
                        editProducto = Producto.objects.get(id=cod_pro)
                        cantAc = editProducto.cantidad
                        cantAc = int(cantAc)
                        editProducto.cantidad = cantAc + devolver
                        editProducto.save()
                    if cant>cantB:
                        pedir = cant - cantB
                        editProducto = Producto.objects.get(id=cod_pro)
                        cantAc = editProducto.cantidad
                        cantAc = int(cantAc)
                        editProducto.cantidad = cantAc - pedir
                        editProducto.save()

                i+=1

            listaProductosPedido2 = PedidoProducto.objects.filter(cantidad=0)
            listaProductosPedido2.delete()



            print 'papaya'
            print id_pedido
            #print listaCantidad
            print 'melon'


            res = {}
            res['respuesta']='hola'
            data = json.dumps(res)

            return HttpResponse(data, content_type='application/json')
        else:
            return Http404


def imprimirPedido(request, idPedido):

    print idPedido

    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "pedidoN"+idPedido+".pdf"  # llamado clientes
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []


    #agregar imagen
    img = Image('media/pdf/imgPDF.png',width=540,height=70,kind='direct',mask='auto',lazy=1,hAlign='CENTER')
    clientes.append(img)


    listapedido = PedidoProducto.objects.filter(pedido_id=idPedido).order_by('id')


    datosTabla = []
    sub = 0

    for a in listapedido:
        productos = Producto.objects.get(id=a.producto_id)

        resul = {}
        resul['id']=productos.id
        resul['stock']=productos.cantidad
        resul['cantidad']=a.cantidad
        resul['producto']=productos.nombre
        resul['precio']=productos.precio
        resul['precio2']=float(productos.precio)*float(a.cantidad)
        resul['precio2']="%.2f" % (resul['precio2'],)
        sub += float(resul['precio2'])
        resul['sub']="%.2f" % (sub,)
        resul['iva']="%.2f" % (sub*0.12)
        total=float(resul['sub'])+float(resul['iva'])
        resul['total']="%.2f" % (total)

        datosTabla.append(resul)


    datosPedido = Pedido.objects.get(id=idPedido)
    datosUsuario = User.object.get(id=datosPedido.usuario_id)

    styles = getSampleStyleSheet()
    header = Paragraph("Informe de Pedido", styles['Heading1'])
    clientes.append(header)
    numPedido = Paragraph("Nº PEDIDO: "+idPedido.__str__(), styles['Normal'])
    clientes.append(numPedido)
    fechaIni = Paragraph("FECHA INICIO: "+datosPedido.fecha_ini.__str__(), styles['Normal'])
    clientes.append(fechaIni)
    fechaFin = Paragraph("FECHA FIN: "+datosPedido.fecha_fin.__str__(), styles['Normal'])
    clientes.append(fechaFin)
    estado = Paragraph("ESTADO: "+datosPedido.estado.__str__(), styles['Normal'])
    clientes.append(estado)
    cedula = Paragraph("CÉDULA: "+datosUsuario.cedula.__str__(), styles['Normal'])
    clientes.append(cedula)
    cliente = Paragraph("CLIENTE: "+datosUsuario.apellidos.__str__()+" "+datosUsuario.nombres.__str__(), styles['Normal'])
    clientes.append(cliente)

    '''
    headings2 = [('Nº PEDIDO: ','HOLA'),('FECHA INICIO: ','LOL')]

    t2 = Table(headings2)
    t2.spaceBefore = -200
    clientes.append(t2)
    '''

    headings = ('Cantidad', 'Producto', 'Precio Unit.', 'Precio Final')
    allproductos = [(p['cantidad'], p['producto'], p['precio'], p['precio2']) for p in datosTabla]

    t = Table([headings] + allproductos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    t.spaceBefore = 20
    t.spaceAfter = 10
    clientes.append(t)

    headings = ('SUBTOTAL', 'IVA', 'TOTAL')
    allproductos = [(datosTabla[0]['sub'], datosTabla[0]['iva'], datosTabla[0]['total'])]

    t = Table([headings] + allproductos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)

    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()


    return response



    '''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'


    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)
    p.setAuthor('G&G by Blessing')
    p.drawImage('media/pdf/disenoPDF01.png',30,640,width=540,height=160,mask=None)
    p.setFont("Helvetica", 25)

    #Titulo
    p.drawString(300, 755, "Informe de Pedido")
    p.line(30,680,570,680)

    p.rect(50,500,500,100)


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont("Helvetica", 12)
    p.drawString(100, 100, "Hello world.")


    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()


    return response
    '''

class vista_pedir(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            id_producto = request.GET['id']
            cantidadPedir = request.GET['cant']
            stock = request.GET['stock']

            cantidadPedir = int(cantidadPedir)
            stock = int(stock)
            print stock-cantidadPedir

            mensaje = ''

            if cantidadPedir > stock:
                mensaje = 'No puede pedir más que el stock'
            else:

                #Capturamos la fecha de hoy
                fechaHoy = datetime.date.today()

                fechaFin = datetime.date.today()+datetime.timedelta(days=3)

                #Revisamos si ya existe un pedido con esta fecha, de no ser asi crearemos uno nuevo
                verPedido = Pedido.objects.filter(usuario_id=request.user.id, fecha_ini=fechaHoy)
                if verPedido:
                    #Chequeo estado del pedido
                    ban = False
                    for ped in verPedido:
                        if ped.estado == 'PENDIENTE':
                            #agrego aqui mis productos
                            ban = True
                            #verificar si ya ha pedido este producto
                            verificarPro = PedidoProducto.objects.filter(pedido_id=ped.id, producto_id=id_producto)
                            if verificarPro:
                                #agrego cantidades a este pedido existente
                                for veriPro in verificarPro:
                                    cantidadAc = veriPro.cantidad
                                    veriPro.cantidad = cantidadAc + cantidadPedir
                                    veriPro.save()
                                    instanciaProducto = Producto.objects.get(id=id_producto)
                                    instanciaProducto.cantidad = stock-cantidadPedir
                                    instanciaProducto.save()
                            else:
                                #creo nuevo
                                pedPro = PedidoProducto(pedido_id=ped.id, producto_id=id_producto, cantidad=cantidadPedir)
                                pedPro.save()
                                instanciaProducto = Producto.objects.get(id=id_producto)
                                instanciaProducto.cantidad = stock-cantidadPedir
                                instanciaProducto.save()
                            break
                    if not ban:
                        #creo un nuevo pedido sin problema
                        nuevoPedido = Pedido(fecha_ini=fechaHoy, fecha_fin=fechaFin, estado='PENDIENTE', usuario_id=request.user.id)
                        nuevoPedido.save()
                        pedPro = PedidoProducto(pedido_id=nuevoPedido.id, producto_id=id_producto, cantidad=cantidadPedir)
                        pedPro.save()
                        instanciaProducto = Producto.objects.get(id=id_producto)
                        instanciaProducto.cantidad = stock-cantidadPedir
                        instanciaProducto.save()
                else:
                    #creo un nuevo pedido sin problema
                    print 'Nuevo pedido'
                    nuevoPedido = Pedido(fecha_ini=fechaHoy, fecha_fin=fechaFin, estado='PENDIENTE', usuario_id=request.user.id)
                    nuevoPedido.save()
                    pedPro = PedidoProducto(pedido_id=nuevoPedido.id, producto_id=id_producto, cantidad=cantidadPedir)
                    pedPro.save()
                    instanciaProducto = Producto.objects.get(id=id_producto)
                    instanciaProducto.cantidad = stock-cantidadPedir
                    instanciaProducto.save()

                mensaje = 'Se agregó a tus pedidos'


            data = json.dumps(mensaje)
            return HttpResponse(data, content_type='application/json')
        else:
            return Http404

def vista_reportes(request):
    return render(request, 'aplicacion/reportes.html'  , context_instance=RequestContext(request))

class vista_reporte1(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            anio = request.GET['ano']
            mes = request.GET['mes']

            datos = []
            productosVendidos = []
            codigoProductosVendidos = []

            listaPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO').order_by('id')

            for pedido in listaPedidos:
                listaProductos = PedidoProducto.objects.filter(pedido_id=pedido.id).order_by('id')
                for producto in listaProductos:
                    res = {}
                    res['codigo']=producto.producto_id
                    res['cantidad']=producto.cantidad
                    codigoProductosVendidos.append(producto.producto_id)
                    productosVendidos.append(res)

            productosNoRepetidos = list(set(codigoProductosVendidos))


            listaProductosVendidos = []

            for proNo in productosNoRepetidos:
                cant = 0
                for pro in productosVendidos:
                    if pro['codigo'] == proNo:
                        cant += int(pro['cantidad'])
                res = {}
                res['codigo']=proNo
                obtenerProducto = Producto.objects.get(id=proNo)
                res['nombre']=obtenerProducto.nombre
                obtenerCategoria = Categoria.objects.get(id=obtenerProducto.categoria_id)
                res['categoria']=obtenerCategoria.nombre
                res['cantidad']=int(cant)
                listaProductosVendidos.append(res)

            print listaProductosVendidos
            listaProductosVendidos.sort(key=lambda x:x['cantidad'])
            listaProductosVendidos.reverse()
            listaProductosVendidos = listaProductosVendidos[:10]#10 productos más vendidos este mes

            print listaProductosVendidos

            datos = listaProductosVendidos


            data = json.dumps(datos)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404

class vista_reporte2(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            anio = request.GET['ano']
            mes = request.GET['mes']

            datos = []
            productosVendidos = []
            codigoProductosVendidos = []

            listaPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO').order_by('id')

            for pedido in listaPedidos:
                listaProductos = PedidoProducto.objects.filter(pedido_id=pedido.id).order_by('id')
                for producto in listaProductos:
                    res = {}
                    res['codigo']=producto.producto_id
                    res['cantidad']=producto.cantidad
                    codigoProductosVendidos.append(producto.producto_id)
                    productosVendidos.append(res)

            productosNoRepetidos = list(set(codigoProductosVendidos))


            listaProductosVendidos = []

            for proNo in productosNoRepetidos:
                cant = 0
                for pro in productosVendidos:
                    if pro['codigo'] == proNo:
                        cant += int(pro['cantidad'])
                res = {}
                res['codigo']=proNo
                obtenerProducto = Producto.objects.get(id=proNo)
                res['nombre']=obtenerProducto.nombre
                obtenerCategoria = Categoria.objects.get(id=obtenerProducto.categoria_id)
                res['categoria']=obtenerCategoria.nombre
                res['cantidad']=int(cant)
                listaProductosVendidos.append(res)

            print listaProductosVendidos
            listaProductosVendidos.sort(key=lambda x:x['cantidad'])
            listaProductosVendidos = listaProductosVendidos[:10]#10 productos más vendidos este mes

            print listaProductosVendidos

            datos = listaProductosVendidos


            data = json.dumps(datos)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404



class vista_reporte3(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            anio = request.GET['ano']
            mes = request.GET['mes']

            datos = []
            listaUsuarios = []

            listaPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO').order_by('id')

            for pedido in listaPedidos:
                listaUsuarios.append(pedido.usuario_id)

            listaUsuarios = list(set(listaUsuarios))

            for codUser in listaUsuarios:
                datosUser = User.object.get(id=codUser)
                numeroPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO', usuario_id=codUser).count()

                res = {}
                res['cedula']=datosUser.cedula
                res['cantidad']=numeroPedidos
                res['apellidos']=datosUser.apellidos
                res['nombres']=datosUser.nombres
                datos.append(res)


            datos.sort(key=lambda x:x['cantidad'])
            datos.reverse()
            datos = datos[:10]

            data = json.dumps(datos)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404

class vista_reporte4(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            anio = request.GET['ano']
            mes = request.GET['mes']

            datos = []
            listaUsuarios = []

            listaPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO').order_by('id')

            for pedido in listaPedidos:
                listaUsuarios.append(pedido.usuario_id)

            listaUsuarios = list(set(listaUsuarios))

            for codUser in listaUsuarios:
                datosUser = User.object.get(id=codUser)
                valorTotalIngreso = 0
                obtenerPedidos = Pedido.objects.filter(fecha_ini__year=anio, fecha_ini__month=mes, estado='VALIDADO', usuario_id=codUser)
                for obPed in obtenerPedidos:
                    obtenerProductosPedido = PedidoProducto.objects.filter(pedido_id=obPed.id)
                    valorPedido = 0
                    valorSub = 0
                    for obPro in obtenerProductosPedido:
                        cantidad = obPro.cantidad
                        producto = obPro.producto_id

                        obtenerProducto = Producto.objects.get(id=producto)
                        valorUnit = obtenerProducto.precio
                        valorSub += (int(cantidad)*float(valorUnit))

                    valorPedido = (valorSub*1.12)
                    valorTotalIngreso += valorPedido



                res = {}
                res['cedula']=datosUser.cedula
                res['cantidad']=float(valorTotalIngreso)

                res['apellidos']=datosUser.apellidos
                res['nombres']=datosUser.nombres
                datos.append(res)

            datos.sort(key=lambda x:x['cantidad'])
            datos.reverse()
            datos = datos[:10]

            for dat in datos:
                dat['cantidad']="%.2f" % (dat['cantidad'])

            data = json.dumps(datos)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404

