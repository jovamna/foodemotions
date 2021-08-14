from django.contrib import admin
from apprecetas.models import Receta, Kategory, Comment
from mptt.admin import MPTTModelAdmin



# Register your models here.
class KategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 40
    list_display = ['parent', 'name', 'slug' ]
    readonly_fields = ('created', 'updated')
    mptt_level_indent = 20
    mptt_indent_field = "some_node_field"


class RecetaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'slug', 'author', 'status', 'kategory')
    ordering = ('author', 'publish')
    search_fields = ('title','content','author__username', 'kategory__name')
    date_hierarchy = 'publish'
    list_filter = ('author__username','kategory__name')
    prepopulated_fields = {'slug': ('title',)}
   
  





admin.site.register(Receta, RecetaAdmin)
admin.site.register(Kategory, MPTTModelAdmin)


admin.site.register(Comment, MPTTModelAdmin)

  






