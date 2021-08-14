from django.contrib import admin
from .models import Kategoria, Post, Comment
from mptt.admin import MPTTModelAdmin


# Register your models here.
class KategoriaAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 40
    list_display = ['parent', 'name', 'slug']
    readonly_fields = ('created', 'updated')


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'slug', 'author', 'status', 'kategoria' )
    ordering = ('author', 'publish')
    search_fields = ('title','content','author__username', 'kategoria__name')
    date_hierarchy = 'publish'
    list_filter = ('author__username','kategoria__name')
    prepopulated_fields = {'slug': ('title',)}




    #def post_categories(self, obj):
        #return ",".join([c.name for c in obj.categories.all().order_by("name") ])
    #post_categories.short_description = "Categorias"    

admin.site.register(Kategoria, MPTTModelAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, MPTTModelAdmin)
