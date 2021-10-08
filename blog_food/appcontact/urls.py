from django.urls import path
from . import views

app_name = 'appcontact'

urlpatterns = [
    path('', views.contact, name="contacto"),
    #path('newsletter/', views.suscribe, name='suscribirse'),
    #path('validate/', views.validate_email, name='validate_email'),
]

# Paths del appfood no se pone de inicio contact solo las '' porque ya lo tenemos puesto en la url principal del proyecto
