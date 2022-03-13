from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Perderpeso
from apprecetas.models import Receta, Kategory
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
#PAGINA PRINCIPAL DE DIETAS ESPECIALES
def categories(request):
    category = Categoria.objects.all()  #SALE TODO!
    cateysubcate = Categoria.objects.filter(
        parent__in=category
    )  # SALE SOLO CATEORIAS QUE TIENEN SUBCATEGORIAS CON SUS SUBCATEGORIAS
    categories = Categoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    category_id = int(
        request.GET.get('categoria_id', default=1)
    )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    post_perder = Perderpeso.objects.all().prefetch_related(
        'categoria', 'categoria__parent')
    f = Categoria.objects.select_related('parent').prefetch_related(
        'name__parent__in')  #SIRVE AQUI
    #PARA EL MENU DE RECETAS SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    print(categories)  #SOLO CATEGORIAS SI HIJOS
    print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_perder)  #TODOS LOS POSTS
    print(f)  #REPITE MUHCO TODO LAS CATEGORIAS Y SUBSCATEGORIAS
    #print(category) #REPITE MUCHO TODO
    print(category_id)  #SACA SOLO EL PRIMER NUMERO

    context = {
        'categories': categories,
        'category': category,
        'cateysubcate': cateysubcate,
        'post_perder': post_perder,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }

    return render(request, 'appperderpeso/plan-comidas-saludables.html',
                  context)


def post(request, category_id=None):
    post_perder = Perderpeso.objects.all()
    categories = Categoria.objects.all()
    pierde = Perderpeso.objects.all().prefetch_related('categoria',
                                                       'categoria__parent')

    if request.method == 'GET':
        category_id = int(request.GET.get('categoria_id', default=1))
        current_category = Categoria.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Categoria.objects.filter(parent__isnull=True)

        print(post_perder)  #TODOS LOS POSTS
        print(categories)
        print(pierde)  #TITULOS DE LOS POSTS
        print(cat)  #SALEN SOLO LAS CATEGORIAS
        print(
            children)  #SALE CATEGORIA CON SUBCATEGORIA ES MEJOR QUE CATEGORIES
        print(current_category)  #categoria actual

        context = {
            'post_perder': post_perder,
            'categories': categories,
            'pierde': pierde,
            'cat': cat,
            'children': children,
        }
        return render(request, 'appperderpeso/posts.html', context)


def post_plan_comida(request, slug=True):
    post = Perderpeso.objects.all().filter(slug=slug)
    categories = Categoria.objects.filter(parent=None)
    kategory = Categoria.objects.all().filter(slug=slug)
    category = Perderpeso.objects.filter(categoria_id__in=kategory)
    post_plan = Perderpeso.objects.all().order_by(
        '-publish')[:1]  #va en el aside

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)

    context = {
        'post': post,
        'post_plan': post_plan,
        'categories': categories,
        'category': category,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }

    print(post)
    print(categories)
    print(category)
    #print(per)

    return render(request, "appperderpeso/post-plan.html", context)


class CategoryRedirectView(RedirectView):
    permanent = False
    query_string = True

    #permanent = True   NO USAR

    def get_redirect_url(self, *args, **kwargs):
        category = get_object_or_404(Categoria, name=self.kwargs['categoria'])
        perder = Perderpeso.objects.filter(
            categoria_id__in=category.get_descendants(include_self=True))

        return reverse('categoria', 'perder', kwargs={'slug': category.slug})


def show_category(request, slug):
    category = Categoria.objects.all().filter(slug=slug)
    post_plan = Perderpeso.objects.filter(
        categoria_id__in=category.get_descendants(
            include_self=True))  #VA CON EL ANTERIOR
    category_deals = Categoria.objects.filter(slug=slug).order_by('slug')
    kategoria = category_deals[0].name
    categoria = category.get_descendants(include_self=True)
    categories = Categoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    cat = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)
    posts = Perderpeso.objects.filter(categoria_id=category).order_by(
        'slug')  #IMPORTANTE

    paginator = Paginator(post_plan, 3)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    print(category_deals)  #CATEGORIA

    print(categories)
    print(post_plan)
    print(categoria)
    print(category)
    print(kategoria)  #CATEGORIA Y SUS HIJOS

    context = {
        'category_deals': category_deals,
        'kategoria': kategoria,
        'post_plan': post_plan,
        'categories': categories,
        'categoria': categoria,
        'recetas': recetas,
        'cat': cat,
        'kategories': kategories,
        'posts': posts,
        'paginator': paginator,
        'pagina': pagina,
        'paginas': paginas,
        'current_page': current_page,
    }
    return render(request, "appperderpeso/categoria.html", context)


def show_subcategory(request, slug=True):
    category_deals = Categoria.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Categoria.objects.all().filter(slug=slug)
    categoria = category.get_descendants(include_self=True)
    perder = Perderpeso.objects.filter(categoria__in=category.get_descendants(
        include_self=True))
    categories = Categoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    category_id = int(request.GET.get('categoria_id', default=1))
 
    posts = Perderpeso.objects.filter(categoria_id=category).order_by(
        'slug')  #IMPORTANTE
        
    post_plan = Perderpeso.objects.filter(categoria_id__in=category.get_descendants(
        include_self=True))  #VA CON EL ANTERIOR
    paginator = Paginator(post_plan, 3)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'category': category,
        'categoria': categoria,
        'perder': perder,
        'categories': categories,
        'post_plan': post_plan,
        'posts': posts,
        'paginator': paginator,
        'pagina': pagina,
        'paginas': paginas,
        'current_page': current_page,
    }

    print(category_deals)
    print(categori)
    print(category)
    print(perder)
    #print(current_category)

    return render(request, "appperderpeso/subcategoria.html", context)
