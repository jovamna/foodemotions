from django.apps import AppConfig


class ApppagesConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'  #Configure DEFAULT_AUTO_FIELD para django 3.2
    name = 'apppages'
    verbose_name = 'Gestor de páginas'
