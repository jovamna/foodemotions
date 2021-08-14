"""blog_food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  #esto es para la carpeta media
from django.contrib.sitemaps.views import sitemap
from appfood.sitemaps import RecetaPostSitemap, RecipePostSitemap, PerderpesoPostSitemap, BlogPostSitemap, PosturismoSitemap, StaticViewSitemap
from appfood import views
import os  #para el secret admin
import environ  #para el secret admin

env = environ.Env()  #para el secret admin
#importante porque si no se pone da fallos
environ.Env.read_env()  #para el secret admin

#*SEO*
sitemaps = {
    'static': StaticViewSitemap,
    'recetas': RecetaPostSitemap,
    'recipes': RecipePostSitemap,
    'perderpeso': PerderpesoPostSitemap,
    'posts': BlogPostSitemap,
    'posturisom': PosturismoSitemap,
}

urlpatterns = [
    # Paths del appfood
    # path('appfood/', include('appfood.urls')), de esta forma no lo encontraria ,hay que dejarlo vacio al principio
    path('', include('appfood.urls', namespace='appfood')),

    # Paths de appservices
    path('services/', include('appservices.urls')),

    # Paths de apppages page nombre de la vista
    path('page/', include('apppages.urls')),

    # Paths de appblog  primero va el nombre de la vista blog
    #IMPORTANTE PONER ASI  path('', include('appblog.urls')), SI NO , NO ENCUENTRA TODOS LOS ARCHIVOS EN APPFOOD
    #path('', include('appblog.urls',  namespace='appblog')),
    path('dietas-especiales-y-alimentacion-sana/',
         include('appblog.urls', namespace='appblog')),

    # Paths de apprecetas  primero va el nombre de la vista blog
    path('recetas-saludables/',
         include('apprecetas.urls', namespace='apprecetas')),

    # Paths de apprecetasalzum  primero va el nombre de la vista blog
    path('recetas-dieteticas/',
         include('apprecetasalzum.urls', namespace='apprecetasalzum')),

    # Paths de appperderpeso primero va el nombre de la vista blog
    path('plan-comidas-saludables/',
         include('appperderpeso.urls', namespace='appperderpeso')),

    # Paths de apppturismo primero va el nombre de la vista blog
    path('noticias-turismo-gastronomico/',
         include('appturismo.urls', namespace='appturismo')),

    # Paths de appcontacts
    path('contacto/', include('appcontact.urls', namespace='appcontact')),

    # Paths del admin
    path(os.environ.get('SECRET_ADMIN_URL') + '/admin/', admin.site.urls),
    #path('admin/', admin.site.urls),
    path('sitemap.xml',
         sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', views.home, name='index'),
    path('recetas_saludables/',
         views.recetas_saludables,
         name="recetas_saludables"),
    path('recetas_dieteticas/',
         views.recetas_dieteticas,
         name="recetas_dieteticas"),
    path('plan_comidas_saludables',
         views.plan_comidas,
         name="plan_comidas_saludables"),
    path('dietas-especiales-y-alimentacion-sana/',
         views.dieta_alimentacion,
         name="dietas-especiales-y-alimentacion-sana"),
    path('noticias_turismo_gastronomico',
         views.noticias_turismo,
         name="noticias_turismo_gastronomico"),
    path('nosotros/', views.nosotros, name="nosotros"),
]

#esto es para la carpeta media cuando este en produccion
if settings.DEBUG:
    from django.conf.urls.static import static
    #from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns (No esty segura si dejarlo)
    #urlpatterns += staticfiles_urlpatterns() (no estoy segura si dejarlo)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    #ahora crear la app services

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#import debug_toolbar
#urlpatterns += [
#path('__debug__/', include(debug_toolbar.urls)),
#]
