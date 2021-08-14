from django.urls import path
from . import views


app_name = 'appcontact'

urlpatterns = [
 
    path('', views.contact, name="contacto"),
  
]



   # Paths del appfood no se pone de inicio contact solo las '' porque ya lo tenemos puesto en la url principal del proyecto