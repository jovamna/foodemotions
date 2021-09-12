from django.urls import path
from . import views

app_name = 'apprecetas'

urlpatterns = [
    path('', views.categorias, name="recetas-saludables"),
    path('receta/<slug:slug>/', views.receta_detail, name="receta"),
    path('addcomment/', views.addcomment, name='addcomment'),
    path(
        'categorias/', views.categorias, name="categorias"
    ),  # category el primero sera el que se vea aunque el html temga otro nombre
    path('categoria/<slug:slug>/', views.categoria, name="categoria"),
    path('subcategoria/<slug:slug>/',
         views.show_subcategory,
         name="subcategoria"),
    #path('', views.recetas, name="recetas"),
]
