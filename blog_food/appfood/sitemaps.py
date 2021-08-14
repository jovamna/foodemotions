# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from apprecetas.models import Receta
from apprecetasalzum.models import Recipe
from appperderpeso.models import Perderpeso
from appblog.models import Post
from appturismo.models import Posturismo





class StaticViewSitemap(Sitemap):
	changefreq = 'monthly'

	def items(self):
		return ['index', 'recetas_saludables', 'recetas_dieteticas', 'plan_comidas_saludables', 'dietas_especiales_y_alimentacion_saludable', 'noticias_turismo_gastronomico', 'nosotros']



	def location(self, item):
	    return reverse(item)

















class RecetaPostSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return Receta.objects.all()

def lastmod(self, obj):
        return obj.updated_on






class RecipePostSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return Recipe.objects.all()

def lastmod(self, obj):
        return obj.updated_on




class PerderpesoPostSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return Perderpeso.objects.all()

def lastmod(self, obj):
        return obj.updated_on




class BlogPostSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return Post.objects.all()

def lastmod(self, obj):
        return obj.updated_on



class PosturismoSitemap(Sitemap):
	changefreq = "weekly"

	def items(self):
		return Posturismo.objects.all()

def lastmod(self, obj):
        return obj.updated_on










