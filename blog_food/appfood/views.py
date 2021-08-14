from django.shortcuts import render
from appblog.models import Post, Kategoria
from appturismo.models import Posturismo, Categori
from appperderpeso.models import Categoria, Perderpeso
from apprecetas.models import Receta, Kategory
from apprecetasalzum.models import Recipe, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

#from operator import attrgetter
#from django.db.models import Q


# Create your views here.
def home(request):  #nombre de la vista
    recetaultimo = Receta.objects.all().order_by('-publish')[2:5]
    perderultimo = Perderpeso.objects.all().order_by('-publish')[:1]
    recipedietaultimo = Recipe.objects.all().order_by('-publish')[1:3]
    postultimo = Post.objects.all().order_by('-publish')[:1]

    receta = Receta.objects.all().order_by('-updated')[:1]
    recetas = Receta.objects.all().order_by('created')[:4]  #RECETAS SALUDABLES
    recipes = Recipe.objects.all().order_by('publish')[:4]
    post_perder = Perderpeso.objects.order_by('publish')[:4]
    perder = Perderpeso.objects.order_by('-publish')[:1]
    posts = Post.objects.order_by('publish')[:4]
    post = Post.objects.order_by('-publish')[:1]
    posturismos = Posturismo.objects.all().order_by('publish')[:3]

    categoria = Categoria.objects.all()  #SALE TODo ESTO ES DE APPERDERPESO
    categorias = Categoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS APPPERDERPESO
    cateysubcategorias = Categoria.objects.filter(
        parent__in=categoria)  # APPPERDERPESO CATEGO Y SUBCATEG

    category = Category.objects.all(
    )  #SALE TODAS LAS CATEGROIAS DE RECETAS DIETETICAS
    categories = Category.objects.filter(
        parent=None)  #SOLO LAS CATEGORIAS RECETAS DIETETICAS
    cateysubcategories = Category.objects.filter(
        parent__in=category)  # CATEORIAS Y SUBCATEGORIAS ZUMOS Y ENSALADAS
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
    kategoria = Kategoria.objects.all()
    subkategoria = Kategoria.objects.filter(parent__in=kategoria)
    kategorias = Kategoria.objects.filter(parent=None)
    #post = Post.objects.filter(kategoria__name="Dietas").order_by('-publish')[:1]
    #perder = Perderpeso.objects.order_by('-categoria__name')[:1]
    #posts = Post.objects.all()
    #perder = Perderpeso.objects.filter(categoria__name="plan").order_by('publish')[:1]

    print(posts)
    print(perder)
    print(receta)

    context = {
        'perderultimo': perderultimo,
        'recetaultimo': recetaultimo,
        'recipedietaultimo': recipedietaultimo,
        'postultimo': postultimo,
        'recipes': recipes,
        'category': category,
        'categories': categories,
        'cateysubcategories': cateysubcategories,
        'recetas': recetas,
        'receta': receta,
        'kategory': kategory,
        'kategories': kategories,
        'post_perder': post_perder,
        'perder': perder,
        'categorias': categorias,
        'cateysubcategorias': cateysubcategorias,
        'posts': posts,
        'post': post,
        'kategoria': kategoria,
        'subkategoria': subkategoria,
        'kategorias': kategorias,
        'posturismos': posturismos,
    }

    return render(request, "appfood/index.html", context)


#recetas = Receta.objects.filter(kategory__name="gastronomia italiana")


#PAGINA PRINCIPAL DE RECETAS SALUDABLES   recetas = Receta.objects.order_by('-publish')[0:8]
def recetas_saludables(request):
    recetas = Receta.objects.all().order_by('slug')[0:5]

    post_recetas = Receta.objects.all().prefetch_related(
        'kategory', 'kategory__parent')
    kategory = Kategory.objects.all()  #SALE TODO!
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    category_id = int(
        request.GET.get('kategory_id', default=1)
    )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Kategory.objects.get(
        pk=category_id
    )  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE
    children = current_category.get_children()
    cateysubcate = Kategory.objects.filter(parent__isnull=True)

    print(children)
    print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    #print(post_recetas)  #TODOS LOS POSTS
    print(current_category)

    context = {
        'recetas': recetas,
        'children': children,
        'cateysubcate': cateysubcate,
        #'post_recetas': post_recetas,
        'current_category': current_category,
        'kategory': kategory,
        'kategories': kategories,
    }

    return render(request, 'appfood/recetas-saludables.html', context)


    #PAGINA PRINCIPAL DE BATIDOS
def recetas_dieteticas(request):
    recipes = Recipe.objects.all().order_by('-slug')[1:6]
    #post_recipes = Recipe.objects.all().prefetch_related(
        #'category', 'category__parent').order_by('-publish')[1:6]
    category = Category.objects.all()  #SALE TODO!
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', default=1))
        current_category = Category.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Category.objects.filter(parent__isnull=True)

    #PARA EL MENU DE RECETSA SALUDABLES
    recetasaludable = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    #print(categories) #SOLO CATEGORIAS SI HIJOS
    #print(children)
    #print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    #print(post_recipes)  #TODOS LOS POSTS
    print(cat)  #TODOS LOS POSTS

    context = {
        'categories': categories,
        'category': category,
        'children': children,
        'recipes': recipes,
        #'post_recipes': post_recipes,
        'cat': cat,
        'recetasaludable': recetasaludable,
        'kategory': kategory,
        'kategories': kategories,
    }

    return render(request, 'appfood/recetas-dieteticas.html', context)


    #PAGINA PRINCIPAL DE DIETAS ESPECIALES
def plan_comidas(request):
    perder = Perderpeso.objects.all().order_by('-publish')[0:6]
    post_perder = Perderpeso.objects.all().prefetch_related(
        'categoria', 'categoria__parent')
    categorias = Categoria.objects.all()  #SALE TODO!
    categoria = Categoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    category_id = int(
        request.GET.get('category_id', default=1)
    )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Categoria.objects.get(
        pk=category_id
    )  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE
    children = current_category.get_children()
    cateysubcate = Categoria.objects.filter(parent__isnull=True)

    post_plan = Perderpeso.objects.filter(
        categoria_id__in=categoria.get_descendants(
            include_self=True))  #VA CON EL ANTERIOR
    categoria_get = categoria.get_descendants(include_self=None)

    f = Categoria.objects.select_related('parent').prefetch_related(
        'name__parent__in')  #SIRVE AQUI
    #PARA EL MENU DE RECETAS SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    category = Category.objects.all()  #SALE TODO!
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    print(categorias)  #SOLO CATEGORIAS SI HIJOS
    print(categoria)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_perder)  #TODOS LOS POSTS
    print(f)  #REPITE MUHCO TODO LAS CATEGORIAS Y SUBSCATEGORIAS

    context = {
        'perder': perder,
        'cateysubcate': cateysubcate,
        'children': children,
        'categorias': categorias,
        'categoria': categoria,
        'categoria_get': categoria_get,
        'post_plan': post_plan,
        'post_perder': post_perder,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        'category': category,
        'categories': categories,
    }

    return render(request, 'appfood/plan-comidas-saludables.html', context)


def dieta_alimentacion(request):
    post_list = Post.objects.all().prefetch_related('kategoria',
                                                    'kategoria__parent')
    kategorias = Kategoria.objects.all()  #SALE TODO!
    kategoria = Kategoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    category = Category.objects.all()  #FIN PARA EL MENU DE RECETSA SALUDABLES

    kategory = Kategory.objects.all()  #A
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(title__icontains=query)

    cat = request.GET.get('cat')
    if cat:
        post_list = post_list.filter(category__pk=cat)

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    category = Category.objects.all()  #SALE TODO!
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    context = {
        'posts': posts,
        'kategoria': kategoria,
        'kategorias': kategorias,
        'category': category,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        'category': category,
        'categories': categories,
    }

    #print(categoria)
    #print(categorias)

    return render(request, "appfood/alimentacion-sana.html", context)


#PAGINA PRINCIPAL DE TURISMO
def noticias_turismo(request):
    post_turismo = Posturismo.objects.all().prefetch_related(
        'categori', 'categori__parent')
    categoris = Categori.objects.all()  #SALE TODO!
    categori = Categori.objects.filter(parent=None)  #SALEN SOLO LAS CATEGORIAS

    post_list = Posturismo.objects.all()

    #PARA EL MENU DE RECETAS SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(title__icontains=query)

    cat = request.GET.get('cat')
    if cat:
        post_list = post_list.filter(categori__pk=cat)

    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    category = Category.objects.all()  #SALE TODO!
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    context = {
        'posts': posts,
        'post_turismo': post_turismo,
        'categoris': categoris,
        'categori': categori,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        'category': category,
        'categories': categories,
    }
    return render(request, "appfood/noticias-turismo-gastronomico.html",
                  context)


def nosotros(request):
    category = Category.objects.all(
    )  #SALE TODAS LAS CATEGROIAS DE RECETAS DIETETICAS
    categories = Category.objects.filter(
        parent=None)  #SOLO LAS CATEGORIAS RECETAS DIETETICAS

    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    context = {
        'categories': categories,
        'category': category,
        'kategory': kategory,
        'kategories': kategories,
    }

    return render(request, "appfood/nosotros.html", context)
