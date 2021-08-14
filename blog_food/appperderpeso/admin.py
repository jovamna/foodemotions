from django.contrib import admin
from appperderpeso.models import Categoria, Perderpeso
from mptt.admin import MPTTModelAdmin

# Register your models here.

class CategoriaAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 40
    list_display = ['parent', 'name', 'slug']
    readonly_fields = ('created', 'updated')

class PerderpesoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'slug', 'author', 'status', 'categoria')
    ordering = ('author', 'publish')
    search_fields = ('title','content','author__username', 'categoria__name')
    date_hierarchy = 'publish'
    list_filter = ('author__username','categoria__name')
    prepopulated_fields = {'slug': ('title',)}

 

    #def perderpeso_category(self, obj):
        #return ",".join([c.name for c in obj.category.all().order_by("name") ])
    #perderpeso_category.short_description = "Categoria"   list display , 'perderpeso_category'



admin.site.register(Perderpeso, PerderpesoAdmin)
admin.site.register(Categoria, MPTTModelAdmin)