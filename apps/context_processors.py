
from .aplicacion.forms import *

#Metodos necesarios para los Procesos
def ver_logeo():
    try:
        form = UsuarioLogin()

    except:
        print 'error proceso'

    return form

def listar_categorias():
    try:
        categorias = Categoria.objects.all().order_by('id')

    except:
        print 'error proceso'

    return categorias

def diezultimosproductos():
    try:
        listaProductos = Producto.objects.all().order_by('id')

        i=len(listaProductos)
        lim=10
        if i < 10:
            lim=i

        ultimosProductos = []

        while lim > 0:
            i -= 1
            res = {}
            listaImagen=Foto.objects.filter(producto_id=listaProductos[i].id)
            for ima in listaImagen:
                res['imagen']=ima.imagen.__str__()

            res['id']=listaProductos[i].id
            res['nombre']=listaProductos[i].nombre
            res['categoria']=listaProductos[i].categoria

            ultimosProductos.append(res)
            lim -= 1

    except:
        print 'error proceso'

    return ultimosProductos




########PROCESOS

#Proceso para formulario de login
def proceso1(request):
    context = {
        'formularioLogeo':ver_logeo(),
    }

    return context

#Proceso para listar categorias en el menu
def proceso2(request):
    context = {
        'listaCategoria_Proceso':listar_categorias(),
        'ultimosProductos':diezultimosproductos(),
    }

    return context