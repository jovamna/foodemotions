from django.contrib import admin
from apprecetasalzum.models import Recipe, Category, Comment
from mptt.admin import MPTTModelAdmin

# Register your models here.
class CategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 40
    list_display = ['parent', 'name', 'slug']
    readonly_fields = ('created', 'updated')



class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'slug', 'author',  'status', 'category')
    ordering = ('author', 'publish')
    search_fields = ('title','content','author__username', 'category__name')
    date_hierarchy = 'publish'
    list_filter = ('author__username','category__name')
    prepopulated_fields = {'slug': ('title',)}
  

  

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Comment, MPTTModelAdmin)

