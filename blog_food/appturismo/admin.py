from django.contrib import admin
from .models import Categori, Posturismo, Comment
from mptt.admin import MPTTModelAdmin


# Register your models here.
class CategoriAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 40
    list_display = ['parent', 'name', 'slug']
    readonly_fields = ('created', 'updated')


class PosturismoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'author', 'status', 'categori' )
    ordering = ('author', 'publish')
    search_fields = ('title','content','author__username', 'categori__name')
    date_hierarchy = 'publish'
    list_filter = ('author__username','categori__name')
    prepopulated_fields = {'slug': ('title',)}




    #def post_categories(self, obj):
        #return ",".join([c.name for c in obj.categories.all().order_by("name") ])
    #post_categories.short_description = "Categorias"    

admin.site.register(Categori, MPTTModelAdmin)
admin.site.register(Posturismo, PosturismoAdmin)
admin.site.register(Comment, MPTTModelAdmin)
