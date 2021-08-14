from django.urls import path
from . import views
from django.conf.urls import include, url

app_name = 'apprecetasalzum'

urlpatterns = [
    path('', views.categorias, name="recetas_dieteticas"),
    path('categoria/<str:slug>/', views.show_category, name="categoria"),
    path('recetas/', views.recipes, name="recetas"),
    path('receta/<slug:slug>/', views.recipe_detail, name='receta'),
    path('subcategoria/<str:slug>/',
         views.show_subcategory,
         name="subcategoria"),

    #path('', views.recetas, name="ensaladasyzumos"),   #al poner el enlace va de esta forma  <a href="{% url 'receta' %}">
    #path('categorias/', views.categorias, name="categorias"),
]