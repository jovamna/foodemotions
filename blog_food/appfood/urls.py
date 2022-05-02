from django.urls import path
from . import views
from django.conf.urls import url, include

app_name = 'appfood'

urlpatterns = [
    path('', views.home, name="index"),
    path('recetas-saludables/',
         views.recetas_saludables,
         name="recetas-saludables"),
    path('recetas-dieteticas',
         views.recetas_dieteticas,
         name="recetas-dieteticas"),
    path('plan-comidas-saludables',
         views.plan_comidas,
         name="plan-comidas-saludables"),
    path('dietas-especiales-y-alimentacion-saludable',
         views.dieta_alimentacion,
         name="dietas-especiales-y-alimentacion-saludable"),
    path('noticias-turismo-gastronomico',
         views.noticias_turismo,
         name="noticias-turismo-gastronomico"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('recetas', views.recetas, name="recetas"),
    path('politica-cookies', views.cookie, name="politica-cookies"),

    #path('search/',views.search, name="search"),
]
