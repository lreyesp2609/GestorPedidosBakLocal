from django.urls import path
from .views import *

urlpatterns = [
    path('crearcat/', CrearCategoriaCombo.as_view(), name='crearcatcombo'),
    path('crearcombo/', CrearCombo.as_view(), name='crearcatcombo'),
    path('editarcombo/<int:combo_id>/', EditarCombo.as_view(), name='editarcombo'),
    path('categoriaExist/', categoriaComboExist.as_view(), name='categoriaComboExist'),
    path('comboExist/', ComboExist.as_view(), name='ComboExist'),
    path('listcategoria/', CategoriasCombosListView.as_view(), name='CategoriasCombosListView'),
    path('ver_combos/', VerCombos.as_view(), name='VerCombos'),
    path('ver_combost/', VerCombosTodo.as_view(), name='VerCombosTodos'),
    path('ver_combosc/<int:categoria_id>/', VerCombosPorCategoria.as_view(), name='ver_combos_por_categoria'),
]
