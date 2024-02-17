
from django.urls import path
from .views import *

urlpatterns = [
    path('creartipop/', CrearTipoProducto.as_view(), name='creartipop'),
    path('crearcategoria/', CrearCategoria.as_view(), name='crearcategoria'),
    path('listatiposycategorias/', ListaTiposYCategorias.as_view(), name='lista_tipos_y_categorias'),
    path('editar_tipo_producto/<int:tipo_producto_id>/', EditarTipoProducto.as_view(), name='editar_tipo_producto'),
    path('editar_categoria/<int:categoria_id>/', EditarCategoria.as_view(), name='editar_categoria'),
    path('crearum/', CrearUnidadMedida.as_view(), name='crearum'),
    path('listarum/', ListarUnidadesMedida.as_view(), name='listar_unidades_medida'),
    path('crearproducto/', CrearProducto.as_view(), name='crearproducto'),
    path('editarum/<int:unidad_id>/', EditarUnidadMedida.as_view(), name='editarum'),
    path('editarproducto/<int:producto_id>/', EditarProducto.as_view(), name='EditarProducto'),
    path('listar/', ListarProductos.as_view(), name='listar_productos'),
    path('listarproductos/', ListaTiposProductos.as_view(), name='ListaTiposProductos'),
    path('tipoProductoExist/', tipoProductoExist.as_view(), name='tipoProductoExist'),
    path('categoriaExist/', CategoriaExist.as_view(), name='CategoriaExist'),
    path('listar_categorias/', ListaCategorias.as_view(), name='ListaCategorias'),
    path('crearcomponente/', CrearComponente.as_view(), name='crearcomponente'),
    path('listarcomponentes/', ListarComponentes.as_view(), name='listar_componentes'),
    path('editarcomponente/<int:id_componente>/', EditarComponentex.as_view(), name='editar_componente'),
    path('eliminarcomponente/', EliminarComponentex.as_view(), name='eliminarcomponente'),
    path('configurarensamble/', CrearEnsambleUnidadMedida.as_view(), name='CrearEnsambleUnidadMedida'),
    path('conversionesum/', ListaConversiones.as_view(), name='ListaConversiones'),
    path('componentenecesario/', ComponentesDisponibles.as_view(), name='ComponentesDisponibles'),
    path('componentenecesariop/', ComponentesDisponiblesPro.as_view(), name='ComponentesDisponiblesPro'),
    path('fabricarcomponente/', FabricarComponente.as_view(), name='FabricarComponente'),
    path('fabricarproducto/', FabricarProducto.as_view(), name='FabricarProducto'),
    path('procesar_productos/', procesar_productos.as_view(), name='procesar_productos'),
    path('EliminarProducto/', EliminarProducto.as_view(), name='EliminarProducto'),
]
