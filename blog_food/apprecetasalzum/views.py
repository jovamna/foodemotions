from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
from apprecetas.models import Receta, Kategory
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from .forms import NewCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here. direccion de los enlaces
#PAGINA PRINCIPAL DE BATIDOS
def categorias(request):
    post_recipes = Recipe.objects.all()
    category = Category.objects.all()  #SALE TODO!
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', default=1))
        current_category = Category.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Category.objects.filter(parent__isnull=True)

    #PARA EL MENU DE RECETSA SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    #print(categories) #SOLO CATEGORIAS SI HIJOS
    #print(children)
    #print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_recipes)  #TODOS LOS POSTS
    print(cat)  #TODOS LOS POSTS

    context = {
        'categories': categories,
        'children': children,
        #'cateysubcate':cateysubcate,
        'post_recipes': post_recipes,
        'cat': cat,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        'category': category,
    }

    return render(request, 'apprecetasalzum/recetas-dieteticas.html', context)


def recipes(request, category_id=None):
    listado_recipes = Recipe.objects.all()
    paginator = Paginator(listado_recipes, 2)
    pagina = request.GET.get("page") or 1
    recipes = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, recipes.paginator.num_pages + 1)
    categories = Category.objects.all()
    recetas = Recipe.objects.all().prefetch_related('category',
                                                    'category__parent')

    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', default=1))
        current_category = Category.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Category.objects.filter(parent__isnull=True)

        print(listado_recipes)  #TODOS LOS POSTS
        print(categories)
        print(recetas)  #TITULOS DE LOS POSTS
        print(cat)  #SALEN SOLO LAS CATEGORIAS
        print(
            children)  #SALE CATEGORIA CON SUBCATEGORIA ES MEJOR QUE CATEGORIES
        print(current_category)

        context = {
            'listado_recipes': listado_recipes,
            'categories': categories,
            'recetas': recetas,
            'cat': cat,
            'recipes': recipes,
            "paginas": paginas,
            "current_page": current_page,
            'children': children,
            'current_category': current_category,
        }

    return render(request, 'apprecetasalzum/recipes.html', context)


def recipe_detail(request, category_id=True, slug=True):
    recipes = Recipe.objects.all().filter(slug=slug)
    categories = Category.objects.filter(parent=None)
    rep = Category.objects.get(pk=1).get_leafnodes()

    postrecipe = Recipe.objects.get(slug=slug)
    allcomments = postrecipe.comments.filter(
        status=True)  #ESTO ES DIFERENTE A COMMENTS

    comment_form = NewCommentForm()
    comments = postrecipe.comments.filter(
        status=True, parent__isnull=True
    )  #ESTO ES DIFERENTE A ALL COMENTS CON ESO EL PARENT PUEDE DIFERENCIARSE DEL COMENT
    if request.method == 'POST':
        # comment has been added                 #AÑADIENDO COMENTARIO
        comment_form = NewCommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15               #RESPONDER A COMENNTARIO
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = comments.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj
            # normal comment
            # create comment object but do not save to database
            new_comment = comment_form.save(commit=False)
            # assign ship to the comment
            #AQUI ME SALE EL FALLO DE QUE LA COLUMNA (1048, "Column 'postrecipe_id' cannot be null")
            #MODIFIQUE EN new_comment.postrecipe
            new_comment.postrecipe = postrecipe
            # save
            new_comment.save()
            return HttpResponseRedirect(
                reverse('apprecetasalzum:receta', args=[postrecipe.slug]))
            #return HttpResponseRedirect(receta_detail.get_absolute_url())
    elif request.method == 'GET':
        #else:
        comment_form = NewCommentForm()

    context = {
        'recipes': recipes,
        'categories': categories,
        'rep': rep,
        'allcomments': allcomments,
        #'comments':  user_comment,
        'comment_form': comment_form,
    }

    print(recipes)
    #print(categories)
    #print(category)
    print(rep)

    return render(request, "apprecetasalzum/recipe-detail.html", context)


def show_category(request, slug):
    category_deals = Category.objects.filter(slug=slug).order_by('slug')
    #category_diet = category_deals[0].name
    category = Category.objects.all().filter(slug=slug)
    post_recipe = Recipe.objects.filter(
        category_id__in=category)  #SE USA CUANDO NO HAY SUBCATEGORIa
    recipe_post = Recipe.objects.filter(
        category_id__in=category.get_descendants(include_self=True))
    categor = category.get_descendants(
        include_self=None)  #IMPORTANTE PARA QUE SALGAN LOS HIJOS
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    cat = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)

    print(category_deals)  #CATEGORIA
    #print(category_diet)  #CATEGORIA
    print(category)  #CATEGORIA Y SUS HIJOS
    print(recipe_post)  #POSTS DE LA CATEGORIA ACTUAL

    context = {
        'category_deals': category_deals,
        'category': category,
        'categor': categor,
        'recipe_post': recipe_post,
        'post_recipe': post_recipe,
        'categories': categories,
        'recetas': recetas,
        'cat': cat,
        'kategories': kategories,
    }
    return render(request, "apprecetasalzum/categoria.html", context)


def show_subcategory(request, slug=True):
    categories = Category.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    category_deals = Category.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Category.objects.all().filter(slug=slug)
    recipes = Recipe.objects.filter(category__in=category.get_descendants(
        include_self=True))

    cati = Category.objects.filter(slug=slug)
    categoria = Category.objects.filter(parent=None).order_by('slug')

    #cater = Category.objects.all().filter(parent=None)
    #kategorie = Category.objects.filter(parent=None).order_by('slug')
    #parent = Category.objects.filter(children__isnull=True)

    context = {
        'recipes': recipes,
        'category_deals': category_deals,
        'categori': categori,
        'category': category,
        'categoria': categoria,
        'categories': categories,
        #'kategorie': kategorie,
        'cati': cati,

        #'parent': parent,
    }

    print(categories)
    print(category_deals)
    print(categori)
    print(category)
    print(cati)
    print(categoria)

    #print(recipes)
    #print(recipe)
    #print(kategorie)
    #print(cat)
    #print(parent)
    return render(request, "apprecetasalzum/subcategoria.html", context)


def categoriasoriginal(request):
    post_recipes = Recipe.objects.all()

    if request.method == 'GET':
        category_id = int(request.GET.get('category_id', default=1))
        current_category = Category.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Category.objects.filter(parent__isnull=True)

        cat = Category.objects.filter(
            parent=None,
            children__in=Category.objects.filter(level=1),
            rght__in=Recipe.objects.all()).distinct()

        category_id = int(
            request.GET.get('category_id', default=1)
        )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
        current_category = Category.objects.get(
            pk=category_id)  #NO VALE SALE LA MISMA CATEGORIA PRIMERA SIEMPRE

    #category = Category.objects.all()  #SALE TODO!
    #cateysubcate = Category.objects.filter(parent__in=category)

    #category = Category.objects.all()  #SALE TODO!
    #categories = Category.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    #category_id = int(request.GET.get('category_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    #current_category = Category.objects.get(pk=category_id)  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE
    #children = current_category.get_children()
    #cateysubcate = Category.objects.filter(parent__in=category) # SALE SOLO CATEORIAS QUE TIENEN SUBCATEGORIAS CON SUS SUBCATEGORIAS
    #post_recipes = Recipe.objects.all().prefetch_related('category','category__parent')
    #post_recipes = Recipe.objects.filter(category_id__in=category.get_descendants(include_self=True))

    #f = Category.objects.select_related('parent').prefetch_related('name__parent__in') #SIRVE AQUI
    #category_deals = Category.objects.filter(slug=slug).order_by('slug')

    #categor = Category.objects.all().filter(slug=slug)
    #PARA EL MENU DE RECETSA SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    #print(categories) #SOLO CATEGORIAS SI HIJOS
    #print(children)
    # print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_recipes)  #TODOS LOS POSTS
    print(cat)  #TODOS LOS POSTS

    #print(categor) #REPITE MUCHO TODO
    #print(category_id) #SACA SOLO EL PRIMER NUMERO
    #print(current_category)

    context = {
        #'categories': categories,
        #'children': children,
        #'cateysubcate':cateysubcate,
        'post_recipes': post_recipes,
        'cat': cat,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        #'category':category,
        #'categor':categor,
        #'current_category': current_category,
    }

    return render(request, 'apprecetasalzum/batidosyensaladas.html', context)
