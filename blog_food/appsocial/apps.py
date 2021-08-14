from django.apps import AppConfig


class AppsocialConfig(AppConfig):
    name = 'appsocial'
    default_auto_field = 'django.db.models.AutoField'  #Configure DEFAULT_AUTO_FIELD para django 3.2
    verbose_name = 'Redes sociales'


#Al iniciar nuevos proyectos en Django 3.2, el tipo predeterminado para las claves primarias se establece en un BigAutoField, que es un entero de 64 bits. Sin embargo, las versiones anteriores establecían el tipo de claves primarias implícitas en números enteros.