from django.shortcuts import render, get_object_or_404
from .models import Posturismo, Categori, Comment
from apprecetas.models import Receta, Kategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .forms import NewCommentForm
from django.http import JsonResponse  #IMPORTANTE PARA LOS COMENTARIOS


# Create your views here.
#PAGINA PRINCIPAL DE TURISMO
def categoris(request):
    post_list = Posturismo.objects.all()
    category_list = Categori.objects.all()
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

    context = {
        'posts': posts,
        'category': category_list,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }
    return render(request, "appturismo/turismo-gastronomico.html", context)


def posts_turismo(request, slug=True):
    posts = Posturismo.objects.all()
    category = Categori.objects.all()  #IMPORTANT PARA LA CATEGORIA
    categoria = Categori.objects.all().filter(
        slug=slug)  #IMPORTANT PARA LA CATEGORIA
    categories = Categori.objects.filter(
        parent=None)  #IMPORTANT PARA LA CATEGORIA
    listado_posts = Posturismo.objects.all()
    paginator = Paginator(listado_posts, 2)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    context = {
        'listado-posts': listado_posts,
        'posts': posts,
        'categories': categories,
        "paginas": paginas,
        "current_page": current_page,
        'category': category,
        'categoria': categoria,
    }

    #print(categories)
    #print(posts)
    #print(current_page)
    #print(current_category)
    #print(children)
    return render(request, "appturismo/posts.html", context)


def post_turismo(request, slug):
    posts = Posturismo.objects.all().filter(slug=slug, status='published')
    categories = Categori.objects.filter(parent=None)
    per = Categori.objects.get(pk=1).get_leafnodes()
    post_turismo = Posturismo.objects.all().order_by(
        '-publish')[:1]  #va en el aside de turismo

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    kategory = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)
    #aqui empieza los coments
    posturismo = Posturismo.objects.get(slug=slug)
    allcomments = posturismo.comments.filter(status=True)
    comment_form = NewCommentForm()
    comments = posturismo.comments.filter(
        status=True, parent__isnull=True)  #este es del modelo comment
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
            new_comment.posturismo = posturismo
            # save
            new_comment.save()
            return HttpResponseRedirect(
                reverse('appturismo:post', args=[posturismo.slug])
            )  #devuelve a la pagina donde esta los comnetarios con el articulo
        elif request.method == 'GET':
            comment_form = NewCommentForm()

    context = {
        'posts': posts,
        'post_turismo': post_turismo,
        'categories': categories,
        'per': per,
        'comment_form': comment_form,
        'allcomments': allcomments,
        'comments': comments,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
    }

    print(posts)
    #print(categories)
    print(comments)
    print(per)

    return render(request, "appturismo/post.html", context)


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


class CategoriRedirectView(RedirectView):
    permanent = False
    query_string = True

    #permanent = True   NO USAR

    def get_redirect_url(self, *args, **kwargs):
        categori = get_object_or_404(Categori, name=self.kwargs['categori'])
        posts = Posturismo.objects.filter(
            categori_id__in=categori.get_descendants(include_self=True))

        return reverse('categoria', 'posts', kwargs={'slug': categori.slug})


def categori(request, slug=True):
    category_deals = Categori.objects.filter(slug=slug).order_by('slug')
    kategoria = category_deals[0].name
    kategory = Categori.objects.all().filter(slug=slug)  #MUY IMPORTANTE
    posturismos = Posturismo.objects.filter(
        categori_id__in=kategory.get_descendants(
            include_self=True))  #MUY IMPORTANTE
    kategor = kategory.get_descendants(include_self=None)
    post_turismo = Posturismo.objects.filter(
        categori_id__in=kategory)  #SE USA CUANDO NO HAY SUBCATEGORIA
    categories = Categori.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS

    recetas = Receta.objects.all()  #RECETAS SALUDABLES
    cat = Kategory.objects.all()  #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None)

    posts = Posturismo.objects.filter(categori_id=kategory).order_by(
        'slug')  #IMPORTANTE VA EN EL TEMPLATE
    paginator = Paginator(posturismos, 3)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

    print(category_deals)  #CATEGORIA
    print(kategory)
    print(categories)  #CATEGORIA Y SUS HIJOS
    print(post_turismo)
    print(posturismos)  #POSTS DE LA CATEGORIA ACTUAL

    context = {
        'category_deals': category_deals,
        'kategoria': kategoria,
        'kategory': kategory,
        'post_turismo': post_turismo,
        'posturismos': posturismos,
        'categories': categories,
        'pagina': pagina,
        'paginas': paginas,
        'current_page': current_page,
        'posts': posts,
        'recetas': recetas,
        'cat': cat,
        'kategories': kategories,
    }
    return render(request, "appturismo/categoria.html", context)


def subcategori(request, slug=True):
    category_deals = Categori.objects.filter(slug=slug).order_by('slug')  #1
    categori = category_deals[0].name  #
    category = Categori.objects.all().filter(slug=slug)  #2
    categoria = category.get_descendants(include_self=True)  #2
    posts = Posturismo.objects.filter(
        categori__in=category.get_descendants(include_self=True))  #2
    categories = Categori.objects.filter(
        parent=None)  #SALEN SOLO LAS CATEGORIAS
    category_id = int(
        request.GET.get('categori_id', default=1)
    )  #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Categori.objects.get(pk=category_id)  #c

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'categoria': categoria,
        'category': category,
        'posts': posts,
        'categories': categories,
    }

    print(category_deals)
    print(categori)
    print(category)
    #print(perder)
    print(current_category)

    return render(request, "appturismo/subcategoria.html", context)


#def categories(request):
#category = Category.objects.order_by('-category_id')
#category = Category.objects.all()
#page = request.GET.get('page', 1)
#paginator = Paginator(category, 20)
#try:
#cat = paginator.page(page)
#except PageNotAnInteger:
#cat = paginator.page(1)
#except EmptyPage:
#cat = paginator.page(paginator.num_apges)
#print(cat)
#return render(request, 'appblog/categorias.html', {'categories': cat})
#post = Posturismo.objects.filter(categori__name='Frutas exoticas')
#posti = Posturismo.objects.filter(categori__name='Restaurantes por el mundo')
#poste = Posturismo.objects.filter(categori__name='Noticias')

#class ProductSearchView(TemplateView):
#template_name ='appblog/search.html'
#class search(ListView):
#model = Post
#template_name = 'appblog/search.html'
