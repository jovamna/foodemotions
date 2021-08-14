from django.urls import path
from . import views
from django.conf.urls import include, url

app_name = 'appturismo'

urlpatterns = [
    path('', views.categoris, name="noticias-turismo-gastronomico"),
    path('posts/', views.posts_turismo, name="posts"),
    path('post/<slug:slug>/', views.post_turismo, name='post'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('categoria/<slug:slug>/', views.categori, name="categoria"),
    path('subcategoria/<slug:slug>/', views.subcategori, name="subcategoria"),
    path('categories/', views.categoris, name="categorias"),
]