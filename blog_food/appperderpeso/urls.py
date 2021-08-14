from django.urls import path
from . import views
from django.conf.urls import include, url

app_name = 'appperderpeso'

urlpatterns = [
    path('', views.categories, name="plan-comidas-saludables"),
    path('posts/', views.post, name="posts"),
    path('post/<slug:slug>/', views.post_plan_comida, name='post'),
    path('categoria/<slug:slug>/', views.show_category, name="categoria"),
    path('subcategoria/<str:slug>/',
         views.show_subcategory,
         name="subcategoria"),
    path('subcategori/<str:slug>/', views.show_subcategory,
         name="subcategori"),

    #path('post/<int:pk>/<str:slug>/',views.perder_detail,name ='post'),
    #path('test/<int:pk>/<str:slug>/',views.single_post,name ='post_detail'),
]