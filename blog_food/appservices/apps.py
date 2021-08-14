from django.apps import AppConfig


class AppservicesConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'  #Configure DEFAULT_AUTO_FIELD para django 3.2
    name = 'appservices'
    verbose_name = 'Gestor de servicios'  #con esto traducimos al español
