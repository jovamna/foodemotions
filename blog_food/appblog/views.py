from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Kategoria, Comment
from .forms import NewCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from apprecetas.models import Receta, Kategory
from appperderpeso.models import Perderpeso, Categoria
from apprecetasalzum.models import Recipe, Category
from appturismo.models import Posturismo, Categori
from django.http import JsonResponse  #IMPORTANTE PARA LOS COMENTARIOS
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import RedirectView
from django.db.models import Prefetch


# Create your views here.
def categories(request):
    post_list = Post.objects.all()
    category_list = Category.objects.all()
    #PARA EL MENU DE RECETSA SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
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

    context = {
        'posts': posts,
        'category': category_list,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }
    return render(request, "appblog/alimentacion-sana.html", context)


def blog(request, slug=True):
    posts = Post.objects.all()
    category = Kategoria.objects.all()  #IMPORTANT PARA LA CATEGORIA
    categoria = Kategoria.objects.all().filter(
        slug=slug)  #IMPORTANT PARA LA CATEGORIA
    categories = Kategoria.objects.filter(
        parent=None)  #IMPORTANT PARA LA CATEGORIA
    listado_posts = Post.objects.all()
    paginator = Paginator(listado_posts, 2)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)
    #PARA EL MENU DE RECETSA SALUDABLES
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

    context = {
        'listado-posts': listado_posts,
        'posts': posts,
        'categories': categories,
        'paginas': paginas,
        'current_page': current_page,
        'category': category,
        'categoria': categoria,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }

    #print(categories)
    #print(posts)
    #print(current_page)
    #print(current_category)
    #print(children)
    return render(request, "appblog/posts.html", context)


def post_detail(request, slug):
    posts = Post.objects.all().filter(slug=slug, status='published')
    categories = Kategoria.objects.filter(parent=None)
    #per=Kategoria.objects.get(pk=1).get_leafnodes()
    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
    post = Post.objects.get(
        slug=slug)  #este codigo es de los comentarios no cambiar get
    pos = Post.objects.order_by('-slug')[:1]  #va en el aside
    posts_comment = Post.objects.all().prefetch_related(
        Prefetch(
            'comments',
            Comment.objects.select_related('user').order_by('-publish')
            [:2],  #-comment_posted_on , post_id
            to_attr='latest_comments',
        ))

    allcomments = post.comments.filter(status=True)

    comment_form = NewCommentForm()
    comments = post.comments.filter(status=True, parent__isnull=True)
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
                parent_obj = Comment.objects.get(id=parent_id)
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
            new_comment.post = post
            # save
            new_comment.save()
            return HttpResponseRedirect(
                reverse('appblog:post', args=[post.slug]))
        elif request.method == 'GET':
            comment_form = NewCommentForm()

    context = {
        'posts': posts,
        'post': post,
        'pos': pos,
        'posts_comment': posts_comment,
        'categories': categories,
        'comment_form': comment_form,
        'allcomments': allcomments,
        'comments': comments,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }

    print(posts)
    #print(comments)
    print(categories)
    print(pos)

    return render(request, "appblog/post.html", context)


def addcomment(request):

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id)
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = NewCommentForm(request.POST)
            print(comment_form)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                result = comment_form.cleaned_data.get('content')
                name = request.user.username
                user_comment.author = request.user
                user_comment.save()
                return JsonResponse({'result': result, 'name': name})


class CategoryRedirectView(RedirectView):
    permanent = False
    query_string = True

    #permanent = True   NO USAR

    def get_redirect_url(self, *args, **kwargs):
        category = get_object_or_404(Kategoria, name=self.kwargs['kategoria'])
        posts = Post.objects.filter(kategoria_id__in=category.get_descendants(
            include_self=True))  #SOLO SIRVE SI HAY SUBCATEGORIAS
        #post =  Post.objects.filter(kategoria_id=self.kwargs.get('pk'))

        return reverse('categoria', 'posts', kwargs={'slug': category.slug})


#CATEGORIA SIN CHILD QUE SE FILTRAN POST POR CATEGORIA
def category(request, slug=True):
    category = Kategoria.objects.all().filter(slug=slug)  #MUY IMPORTANTE PARA OBTNER POSTS SEGUN CATEGORIA AUQNUE NO HAYA SUBCATEGORIAS
    post_dieta = Post.objects.filter(kategoria_id__in=category.get_descendants(
        include_self=True))  #VA CON EL ANTERIOR
    category_deals = Kategoria.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name

    categor = category.get_descendants(
        include_self=None)  #IMPORTANTE PARA LOS CHILDS DE LA MISMA CATEGORIA
    categories = Kategoria.objects.filter(
        parent=None)  #SCATEGORIAS si pongo True ya no salen las categorias
    #post = Post.objects.filter(
    #kategoria_id__in=category)  #SE USA CUANDO NO HAY SUBCATEGORIA

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    cat = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)

    posts = Post.objects.filter(kategoria_id=category).order_by(
        'slug')  #IMPORTANTE
    paginator = Paginator(post_dieta, 3)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    print(category_deals)  #CATEGORIA
    print(categori)  #CATEGORIA
    print(category)  #CATEGORIA Y SUS HIJOS
    #print(post)  #POSTS DE LA CATEGORIA ACTUAL
    print(categories)
    print(posts)
    print(categor)

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'category': category,
        'post_dieta': post_dieta,
        'categories': categories,
        'posts': posts,
        'pagina': pagina,
        'paginas': paginas,
        'current_page': current_page,
        'category': category,
        'recetas': recetas,
        'cat': cat,
        'kategories': kategories,
    }

    return render(request, "appblog/categoria.html", context)


def subcategory(request, slug=True):
    category_deals = Kategoria.objects.filter(slug=slug).order_by('slug')  #1
    categori = category_deals[0].name  #
    category = Kategoria.objects.all().filter(slug=slug)  #2
    categoria = category.get_descendants(include_self=True)  #2
    posts = Post.objects.filter(kategoria__in=category.get_descendants(include_self=True))
    categorias = Kategoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    kategorias = Kategoria.objects.all()
    category_id = int(
        request.GET.get('categoria_id', default=1)
    )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Kategoria.objects.get(pk=category_id)  #c
    post_kategoria = Post.objects.filter(kategoria_id=category).order_by(
        'slug')  #IMPORTANTE

    post_dieta = Post.objects.filter(kategoria_id__in=category.get_descendants(
        include_self=True))  #VA CON EL ANTERIOR
    paginator = Paginator(post_dieta, 3)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'categoria': categoria,
        'category': category,
        'posts': posts,
        'categorias': categorias,
        'kategorias': kategorias,
        'post_dieta': post_dieta,
        'post_kategoria': post_kategoria,
        'pagina': pagina,
        'paginas': paginas,
        'current_page': current_page,
    }

    print(category_deals)
    print(categori)
    print(category)
    print(posts)
    print(current_category)
    print(categorias)

    return render(request, "appblog/subcategoria.html", context)


def search(request):  # new
    query = request.GET.get("q", "")
    posts = Post.objects.all()
    recetas = Receta.objects.all()
    perderpes = Perderpeso.objects.all()
    recipes = Recipe.objects.all()
    notituris = Posturismo.objects.all()
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query)
            | Q(description__iexact=query)).order_by('kategoria').distinct()
        recetas = Receta.objects.filter(
            Q(title__icontains=query)
            | Q(description__iexact=query)).order_by('-updated').distinct()
        perderpes = Perderpeso.objects.filter(
            Q(title__icontains=query)
            | Q(description__iexact=query)).order_by('-updated').distinct()
        recipes = Recipe.objects.filter(
            Q(title__icontains=query)
            | Q(description__iexact=query)).distinct()
        notituris = Posturismo.objects.filter(
            Q(title__icontains=query) | Q(description__iexact=query)
            | Q(contentone__icontains=query) | Q(narrativa__icontains=query)
            | Q(contentwo__icontains=query)
            | Q(contenthree__iexact=query)).distinct()

    else:
        posts = []
        recetas = []
        perderpes = []
        recipes = []
        notituris = []

    context = {
        'posts': posts,
        'recetas': recetas,
        'perderpes': perderpes,
        'recipes': recipes,
        'notituris': notituris,
        'query': query,
    }

    #queryset_list = list(chain(posts, recetas, recipes))

    #posts = Post.objects.filter().order_by('title')
    print(request.GET)
    print(query)
    print(posts)
    print(recetas)
    print(perderpes)
    print(recipes)
    print(notituris)

    return render(request, "appblog/search.html", context)


#NO USADO SOLO SIRVE PARA LA CATEGORIA ACTUAL SI TIENE SUBCATEGORIA
def categorit(request, slug=True):
    category_deals = Kategoria.objects.filter(slug=slug).order_by('slug')
    kategoria = category_deals[0].name
    category = Kategoria.objects.all().filter(slug=slug)
    category = category.get_descendants(include_self=None)
    posts = Post.objects.filter(kategoria_id__in=category.get_descendants(
        include_self=True))
    post = Post.objects.all()
    categorias = Kategoria.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    print(category_deals)  #CATEGORIA
    print(kategoria)  #CATEGORIA
    print(category)  #CATEGORIA Y SUS HIJOS
    print(posts)  #POSTS DE LA CATEGORIA ACTUAL
    print(post)

    context = {
        'category_deals': category_deals,
        'kategoria': kategoria,
        'category': category,
        'posts': posts,
        'categorias': categorias,
        'post': post,
    }
    return render(request, "appblog/categoria.html", context)
