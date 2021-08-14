from django.shortcuts import render, get_object_or_404
from .models import Receta, Kategory, Comment
from django.core.paginator import Paginator
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .forms import NewCommentForm
from django.http import JsonResponse





# Create your views here. direccion de los enlaces
#PAGINA PRINCIPAL DE RECETAS SALUDABLES
def categorias(request):
    post_recetas = Receta.objects.all().prefetch_related('kategory','kategory__parent')
    kategory = Kategory.objects.all()  #SALE TODO!
    kategories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    category_id = int(request.GET.get('kategory_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Kategory.objects.get(pk=category_id)  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE
    children = current_category.get_children()
    cateysubcate = Kategory.objects.filter(parent__isnull=True) 
    
    
    #PARA EL MENU DE RECETSA SALUDABLES
    #kategory =Kategory.objects.all() #RECETAS SALUDABLES
    #kategories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
  
    #print(categories) #SOLO CATEGORIAS SI HIJOS
    print(children)
    print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_recetas) #TODOS LOS POSTS
    print(current_category)
   
   
    context = {
        'children': children,
        'cateysubcate':cateysubcate,
        'post_recetas': post_recetas,
        'current_category':current_category,
        'kategory': kategory,
        'kategories': kategories,
        
    }
    
    return render(request, 'apprecetas/recetas-saludables.html', context)




def recetas(request,category_id=None):
    listado_recetas = Receta.objects.all()
    categories = Kategory.objects.all()
    paginator = Paginator(listado_recetas, 2)
    pagina = request.GET.get("page") or 1
    recetas = paginator.get_page(pagina) 
    current_page = int(pagina)
    paginas = range(1, recetas.paginator.num_pages + 1)
    posts = Receta.objects.all().prefetch_related('kategory','kategory__parent') 
    
    if request.method == 'GET':
        category_id = int(request.GET.get('kategory_id', default=1))
        current_category = Kategory.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Kategory.objects.filter(parent__isnull=True) 

    print(posts)
    print(children)
    print(cat)
    print(category_id)
    print(categories)
    print(current_category)

     
    context= {
        'recetas':recetas,
        "paginas": paginas,
        "current_page": current_page,
        'categories':categories,
        'current_category':  current_category,
    }
    return render(request, "apprecetas/recetas.html", context)
 



def receta_detail(request,kategory_id=True,slug=True):
    post_receta = Receta.objects.all().filter(slug=slug)
    categories = Kategory.objects.filter(parent=None)
    cat=Kategory.objects.get(pk=1).get_leafnodes()
    post=Receta.objects.get(slug=slug)
    post_meta = post.convert_in_meta    #SEO
  
   
    allcomments = post.comments.filter(status=True) #ESTO ES DIFERENTE A COMMENTS

    comment_form = NewCommentForm()
    comments = post.comments.filter(status=True, parent__isnull=True) #ESTO ES DIFERENTE A ALL COMENTS CON ESO EL PARENT PUEDE DIFERENCIARSE DEL COMENT
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
            return HttpResponseRedirect(reverse('apprecetas:receta', args=[post.slug]))
            #return HttpResponseRedirect(receta_detail.get_absolute_url())
    elif request.method == 'GET':        
    #else:
        comment_form = NewCommentForm()
  

    context = {
                'post_receta':post_receta,
                'categories': categories,
                'cat':cat,
                'allcomments': allcomments,
                #'comments':  user_comment,
                'comment_form': comment_form,
                'post_meta': post_meta,
            
             }
                    
    print(post_receta)
    print(categories)
    #print(allcomments)
    print(comments)
    print(cat)
    print(comment_form)
    #print(parent_id)


    return render(request, "apprecetas/receta.html", context)



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
                   user = request.user.username
                   user_comment.author = request.user
                   user_comment.save()
                   return JsonResponse({'result': result, 'user': user})





class CategoryRedirectView(RedirectView):
    permanent = False
    query_string = True
    #permanent = True

    def get_redirect_url(self, *args, **kwargs):
        category = get_object_or_404(Kategory, name=self.kwargs['category'])
        receta = Receta.objects.filter(kategory_id__in=category.get_descendants(include_self=True))
        post_receta = Receta.objects.filter(Kategory_id=self.kwargs.get('slug'))
      
        return reverse('categoria','receta', kwargs={'slug': category.slug})

def categoria(request,slug=True):   
    category_deals = Kategory.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Kategory.objects.all().filter(slug=slug)
    catego = category.get_descendants(include_self=None)
    receta = Receta.objects.filter(kategory_id__in=category.get_descendants(include_self=True))
    categories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    #category = category.get_descendants(include_self=None)  /*CREO IMPORTANTE NO BORRAR
  
    print(category_deals) #CATEGORIA
    print(categori)       #CATEGORIA
    print(category)       #CATEGORIA Y SUS HIJOS
    #print(receta)    #POSTS DE LA CATEGORIA ACTUAL
 
    context={
        'category_deals': category_deals,
        'categori':categori,
        'catego':catego,
        'category':category,
        'receta':receta,
        'categories' : categories,
    }
    return render(request,"apprecetas/categoria.html", context)





def show_subcategory(request, category_id=True, slug=True):
    receta = Receta.objects.filter(kategory_id=category_id)   
    category_deals = Kategory.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Kategory.objects.all().filter(slug=slug)
    category = category.get_descendants(include_self=True)
    post =  Receta.objects.filter(kategory_id__in=category) #SE USA CUANDO NO HAY SUBCATEGORIA
    recetas = Receta.objects.filter(kategory__in=category.get_descendants(include_self=True))
    categoria = Kategory.objects.filter(parent=None).order_by('slug')#SALEN SOLO LAS CATEGORIAS
    subcategory=Kategory.objects.exclude(parent=None)
    categorie = categoria[0]
    
    category_id = int(request.GET.get('category_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Kategory.objects.get(pk=category_id)  #c
   
 

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'category': category,
        'recetas':recetas,
        'post': post,
        'current_category': current_category,
        'categoria' : categoria,
        'subcategory' : subcategory,
        'receta':receta,
        }     

      
    print(category_deals)
    print(categori)
    print(category)
    print(recetas)
   
    
    print(categoria)
    print(subcategory)
    print(category_id)
    print(current_category)
    print(receta)
   
    return render(request,"apprecetas/subcategoria.html", context)










#def receta_detail(request, slug):
   #receta = get_object_or_404(Receta, slug=slug)
   #receta = Receta.objects.get(id=idreceta)
   #print(receta)
   #return render(request, "apprecetas/receta.html", {'receta':receta})



def categoriasoriginal(request):
    category = Kategory.objects.all()  #SALE TODO!
    categories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    category_id = int(request.GET.get('kategory_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    current_category = Kategory.objects.get(pk=category_id)  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE
    children = current_category.get_children()
    cateysubcate = Kategory.objects.filter(parent__in=category) # SALE SOLO CATEORIAS QUE TIENEN SUBCATEGORIAS CON SUS SUBCATEGORIAS
    post_recetas = Receta.objects.all().prefetch_related('kategory','kategory__parent')
    recetas = Receta.objects.filter(kategory__in=category.get_descendants(include_self=True))
    f = Kategory.objects.select_related('parent').prefetch_related('name__parent__in') #SIRVE AQUI
    post_receta = Receta.objects.all()
    #PARA EL MENU DE RECETSA SALUDABLES
    kategory =Kategory.objects.all() #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES
  

   
    print(categories) #SOLO CATEGORIAS SI HIJOS
    print(children)
    print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_recetas) #TODOS LOS POSTS
    print(current_category)
    print(post_receta)
  
  
   
    context = {
        'categories': categories,
        'children': children,
        'cateysubcate':cateysubcate,
        'post_recetas': post_recetas,
        'post_receta': post_receta,
        'current_category':current_category,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        
    }
    
    return render(request, 'apprecetas/recetas_saludablesorigial.html', context)


















































#def categoria(request, pk):
    #categoria = get_object_or_404(Categoria, id=pk)   #retrive single category
    #print(categoria)
    #return render(request, 'apprecetas/categoria.html', {'categoria': categoria})



#def categorias(request):
    #recetas = Receta.objects.all()
    #categorias_recetas = Category.objects.all()
    #content = {
        #'recetas': recetas,
        #'categorias_recetas':categorias_recetas,
        #'title': 'Recetas'
    #}
    #print(content)
    #return render(request, 'apprecetas/categorias.html', content)  
    
    
 
   