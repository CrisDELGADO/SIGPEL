# -*- coding: utf-8
from django.conf.urls import patterns,include, url
from .views import *

urlpatterns = patterns('',
    url(r'^$',vista_inicio),
    url(r'^login/$',vista_login.as_view()),
    url(r'^usuario/$',vista_usuario),
    url(r'^usuario_ajax/$',vista_usuario_ajax),
    url(r'^nuevousuario_ajax/$',vista_nuevoUsuario_ajax),
    url(r'^usuario/provincia/$',vista_provincia.as_view()),
    url(r'^misdatos/$',vista_misDatos),
    url(r'^misdatos_ajax/$',vista_misDatos_ajax.as_view()),
    url(r'^misdatos_contra_ajax/$',vista_misDatos_contra_ajax.as_view()),
    #url(r'^misdatos/(?P<id_user>.*)/$',vista_misDatos),
    url(r'^productos/$',vista_productos),
    url(r'^productos/categorias/$',vista_productos_ajax.as_view()),
    url(r'^productos/categoria/(?P<id_categoria>.*)/$',vista_productos_categoria),
    url(r'^productos/detalle/(?P<id_producto>.*)/$',vista_producto_detalle),

    url(r'^productos/filtrar/$',vista_productos_filtrar.as_view()),

    url(r'^informacion/$',vista_informacion),

    url(r'^verificarFecha/$',vista_verificar_fecha.as_view()),

    url(r'^mispedidos/$',vista_mispedidos),
    url(r'^mispedidos/pedido/detalle/$',vista_pedidoDetalle.as_view()),
    url(r'^mispedidos/pedido/editar/$',vista_pedidoDetalleEditar.as_view()),
    url(r'^mispedidos/pedido/cancelar/$',vista_pedidoDetalleCancelar.as_view()),
    url(r'^mispedidos/pedido/imprimir/(?P<idPedido>.*)/$',imprimirPedido, name='imprimirPedido'),

    url(r'^gestionarpedidos/$',vista_gestionarpedidos),
    url(r'^gestionarpedidos/pedidosCedula/$',vista_gestionar_VerPedidos.as_view()),
    url(r'^gestionarpedidos/validarPedido/$',vista_gestionar_ValidarPedido.as_view()),

    url(r'^productos/pedir/$',vista_pedir.as_view()),

    url(r'^administrar/$',vista_administrar),
    url(r'^administrar-categoria/$',vista_administrar_categoria),
    url(r'^administrar-categoria/listaCategorias/$',vista_listaCategorias_admin.as_view()),
    url(r'^administrar-categoria/agregar/$',vista_administrar_categoria_agregar.as_view()),
    url(r'^administrar-categoria/editar/$',vista_administrar_categoria_editar.as_view()),
    url(r'^administrar-categoria/eliminar/$',vista_administrar_categoria_eliminar.as_view()),
    url(r'^administrar-producto/$',vista_administrar_producto),
    url(r'^administrar-producto/agregar/$',vista_administrar_producto_agregar.as_view()),
    url(r'^administrar-producto/listaProductos/$',vista_listaProductos_admin.as_view()),
    url(r'^administrar-producto/editar/$',vista_administrar_producto_editar.as_view()),
    url(r'^administrar-producto/eliminar/$',vista_administrar_producto_eliminar.as_view()),
    url(r'^administrar-usuario/$',vista_administrar_usuario),
    url(r'^administrar-usuario/estado/$',vista_administrar_usuario_estado.as_view()),
    url(r'^administrar-usuario/listaUsuarios/$',vista_administrar_usuario_listaUsuarios.as_view()),

    url(r'^reportes/$',vista_reportes),
    url(r'^reportes/reporte1/$',vista_reporte1.as_view()),
    url(r'^reportes/reporte2/$',vista_reporte2.as_view()),
    url(r'^reportes/reporte3/$',vista_reporte3.as_view()),
    url(r'^reportes/reporte4/$',vista_reporte4.as_view()),

    url(r'^salir/',cerrarSesion),
)