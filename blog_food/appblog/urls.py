from django.urls import path
from . import views
from .views import search
from .views import post_detail
from django.conf.urls import include, url

app_name = 'appblog'

urlpatterns = [
    path('',
         views.categories,
         name="dietas-especiales-y-alimentacion-saludable"),
    path('posts/', views.blog, name="posts"),
    path('post/<slug:slug>/', views.post_detail, name='post'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('categoria/<slug:slug>/', views.category, name="categoria"),
    path('subcategoria/<slug:slug>/', views.subcategory, name="subcategoria"),
    path('search/', views.search, name="search"),
]