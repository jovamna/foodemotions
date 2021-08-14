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
    cateysubcate = Categoria.objects.filter(parent__in=category) # SALE SOLO CATEORIAS QUE TIENEN SUBCATEGORIAS CON SUS SUBCATEGORIAS
    categories = Categoria.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    category_id = int(request.GET.get('categoria_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    post_perder = Perderpeso.objects.all().prefetch_related('categoria','categoria__parent')
    f = Categoria.objects.select_related('parent').prefetch_related('name__parent__in') #SIRVE AQUI
    #PARA EL MENU DE RECETAS SALUDABLES
    recetas = Receta.objects.all() #RECETAS SALUDABLES
    kategory =Kategory.objects.all() #RECETAS SALUDABLES
    kategories = Kategory.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS RECETAS SALUDABLES

   
    print(categories) #SOLO CATEGORIAS SI HIJOS
    print(cateysubcate)  #CATEGORIAS CON SUS SUBCATEGORIAS
    print(post_perder) #TODOS LOS POSTS
    print(f)  #REPITE MUHCO TODO LAS CATEGORIAS Y SUBSCATEGORIAS
    #print(category) #REPITE MUCHO TODO
    print(category_id) #SACA SOLO EL PRIMER NUMERO
  
   
    context = {
        'categories': categories,
        'category':category,
        'cateysubcate':cateysubcate,
        'post_perder': post_perder,
        'recetas': recetas,
        'kategory': kategory,
        'kategories': kategories,
        
    }
    
    return render(request, 'appperderpeso/plan-comidas-saludables.html', context)








def post(request, category_id=None):
    post_perder=Perderpeso.objects.all()
    categories = Categoria.objects.all()
    pierde = Perderpeso.objects.all().prefetch_related('categoria','categoria__parent')
  
    
    if request.method == 'GET':
        category_id = int(request.GET.get('categoria_id', default=1))
        current_category = Categoria.objects.get(pk=category_id)
        children = current_category.get_children()
        cat = Categoria.objects.filter(parent__isnull=True)
    

      
        print(post_perder)   #TODOS LOS POSTS   
        print(categories)
        print(pierde)  #TITULOS DE LOS POSTS
        print(cat)           #SALEN SOLO LAS CATEGORIAS
        print(children)  #SALE CATEGORIA CON SUBCATEGORIA ES MEJOR QUE CATEGORIES
        print(current_category)   #categoria actual

        context = {
            'post_perder':post_perder,
            'categories': categories,
            'pierde':pierde,
            'cat':cat,
            'children':children,
           
        }
        return render(request, 'appperderpeso/posts.html', context)

   
def post_plan_comida(request, slug=True):
    post = Perderpeso.objects.all().filter(slug=slug)
    categories = Categoria.objects.filter(parent=None)
    kategory = Categoria.objects.all().filter(slug=slug)
    category =  Perderpeso.objects.filter(categoria_id__in=kategory)


    context = {
            'post':post,
            'categories': categories,
            'category':category,
        
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
        perder = Perderpeso.objects.filter(categoria_id__in=category.get_descendants(include_self=True))
      
        return reverse('categoria','perder', kwargs={'slug': category.slug})


def show_category(request, slug=True):   
    category_deals = Categoria.objects.filter(slug=slug).order_by('slug')
    kategoria = category_deals[0].name
    category = Categoria.objects.all().filter(slug=slug) #MUY IMPORTANTE PARA OBTNER POSTS SEGUN CATEGORIA AUQNUE NO HAYA SUBCATEGORIAS
    post_plan = Perderpeso.objects.filter(categoria_id__in=category.get_descendants(include_self=True)) #VA CON EL ANTERIOR
    categoria = category.get_descendants(include_self=None)
    categories = Categoria.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    

    listado_posts = Perderpeso.objects.all()
    paginator = Paginator(listado_posts, 2)
    pagina = request.GET.get("page") or 1
    posts = paginator.get_page(pagina) 
    current_page = int(pagina)
    paginas = range(1, posts.paginator.num_pages + 1)

   
    print(category_deals) #CATEGORIA
    print(kategoria)       #CATEGORIA Y SUS HIJOS
 
    

    context={
        'category_deals': category_deals,
        'kategoria':kategoria,
        'post_plan':post_plan,
        'categories': categories,
        'listado_posts': listado_posts,
        'paginator' : paginator,
        'categoria'  :  categoria,
    }
    return render(request,"appperderpeso/categoria.html", context)



def show_subcategory(request,slug=True):   
    category_deals = Categoria.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Categoria.objects.all().filter(slug=slug)
    categoria = category.get_descendants(include_self=True)
    perder = Perderpeso.objects.filter(categoria__in=category.get_descendants(include_self=True))
    categories = Categoria.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
    category_id = int(request.GET.get('categoria_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    #current_category = Categoria.objects.get(pk=category_id)  #c
 

    context = {
        'category_deals': category_deals,
        'categori': categori,
        'category': category,
        'categoria': categoria,
        'perder':perder,
        'categories':categories,
        }     

      
    print(category_deals)
    print(categori)
    print(category)
    print(perder)
    #print(current_category)
   
    return render(request,"appperderpeso/subcategoria.html", context)














    #slug = category_slug
    #if slug:
        #category_s = slug = slug   
        #per = pierde.filter(category = category_s)
        
    #if request.method == 'GET':
        #category_id = int(request.GET.get('category_id', default=1))
        #current_category = Category.objects.get(pk=category_id)
        
        #children = current_category.get_children()
        #ancestors = current_category.get_ancestors()
        #perder = current_category.perderpeso.all()




    #d=Perderpeso.objects.filter(category_id=category_id)
    #p=Perderpeso.objects.filter(category__in=Category.objects.get(pk=2)\
    #.get_descendants(include_self=True))
   
    #if request.method == 'GET':
         #category_id= int(request.GET.get('parent_id',default=active))
        #post_id = str(request.GET.get('id', default=1))
        #current_post = Perderpeso.objects.get(pk=post_id)

   
   


     #category_id = int(request.GET.get('category_id', default=1)) #ESTE ME PARECE LIMITA A QUE SOLO SALGA LA PRIMERA CATEGORIA
    #current_category = Category.objects.get(pk=category_id)  #creo van juntos con category_id SALE SOLO LA CATEGORIA ACTUAL noMBRE

    #children = current_category.get_children() #SALE LA CATEORIA ACTUAL CON SU HIJA

    #pera = Category.objects.filter(children__in=category.get_descendants(True)) #SALEN LAS CATEGORIAS QUE SOLO TIENEN SUBCATEGORIAS(NO INCLUYE SUBCATEGORIA)

    #categoria=Category.objects.filter(parent=None) #SALEN TODAS LAS CATEGORIAS CON O SIN SUBCATEG(PERO NO SE VE ESCRITO LAS SUBCATEGORIAS)
    #perk = Category.objects.filter(parent__isnull=category.get_descendants(True))  #SALEN TODAS LAS CATEGORIAS CON O SIN SUBCATEG(PERO NO SE VE ESCRITO AS SUBCATEGORIAS)
    #cat = Category.objects.filter(parent__isnull=True) #PERDER PESO Y PLAN COMPLETO PARA ADELGAZAR
    #catego = Category.objects.filter(parent=category_slug) #CATEGORIA PERDER PESO Y PLAN COMPLETO PARA ADELGAZAR

    #sub_categoria=Category.objects.exclude(parent=None) #CATEGORIA PERDER PESO SUBCATEGORIA ALIMENTOS HIPOCALORICOS CATEGORIA PLAN COMPLETO PATA ADELGAZAR SUBCATEGORIA ALIMENTACION DETOX
    #pero = Category.objects.filter(level__in=category.get_descendants(True))   # SALEN CATEGORIAS Y SUBCATEGORIAS EL QUE NO TIENE SUBCATEGORIA NO SALE
    #perd = Category.objects.filter(parent_id__in=category.get_descendants(True)) # ""
    
    #perc = Category.objects.filter(parent__in=category.get_descendants(True)) # ""

   

def show_categoryoriginal(request,slug=True):   
    category_deals = Categoria.objects.filter(slug=slug).order_by('slug')
    categori = category_deals[0].name
    category = Categoria.objects.all().filter(slug=slug)
    category = category.get_descendants(include_self=None)
    perder = Perderpeso.objects.filter(categoria_id__in=category.get_descendants(include_self=True))
    categories = Categoria.objects.filter(parent=None) #SALEN SOLO LAS CATEGORIAS
   
    
    #print(category_deals) #CATEGORIA
    #print(categori)       #CATEGORIA
    print(category)       #CATEGORIA Y SUS HIJOS
    print(perder)    #POSTS DE LA CATEGORIA ACTUAL
    
    
  

    context={
        'category_deals': category_deals,
        'categori':categori,
        'category':category,
        'perder':perder,
        'categories': categories,
    }
    return render(request,"appperderpeso/categoria.html", context)






   







    

      
    
    #catig=Category.objects.filter(slug=slug)
    #parent = get_object_or_404(Category, slug=slug, parent=parent)MAL HECHO
    #parent = Category.objects.filter(slug__in=slug, parent=None).first()
    #self.catig = Category.objects.get(slug=self.kwargs['slug'])
    #catego = get_object_or_404(Category, slug=slug)
    #child = category.get_children()
    #if not child:
        #child = category.get_siblings()
       
    #category_id = int(request.GET.get('category_id', default=1))
    #current_category = Category.objects.get(pk=category_id)
    #children = current_category.get_children()
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(cat)
    print(p) 
    #print(categories)
    #print(slug)
    #print(category_id)
    #print(categoria)
    print(category)
     
    #print(current_category) 
    #print(children)
    #print(perder)
    

    
    context={
        #'categories': children,
        #'children': categories,
        #'current_category': current_category,
        #'ancestors': ancestors,
        #'parent':categories,
        #'catig':catig,
        #'categoria':categoria,
        #'cat':cat,
        'category':category,
        
    }
    return render(request,"appperderpeso/categoriaDOS.html", context)



















#def categories(request, category_id):
    #pk = request.GET.get('pk')  //ESTO NO ME FUNCINA A MI MODELO
    #cat = get_object_or_404(Category, pk=category_id)  #probar esto
    #ancestors = current_category.get_ancestors()  #NO VA
    #print(categories)
    #print(ancestors)
    #context={
        #'categories':categories,
    #}
    #return render(request, 'appperderpeso/categories.html', context)


#products_category = Product.objects.filter(category__name=cats)






























    #def post(request):
        #post_perder=Perderpeso.objects.all()
        #cat=Category.objects.all()
        #perder=Category.objects.filter(
        #parent=None,  # must be root category
        #children__in=Category.objects.filter(level=1),  # must have at least one sub-category
        #perderpeso__in=Perderpeso.objects.all()  # must have at least one product
#)
        #print(post_perder)
        #print(cat)
        #print(categ)
        #print(perder)
        #context={
           #'post_perder':post_perder,
           #'cat':cat,
        #}

    #return render(request, 'appperderpeso/perderpeso.html', context)




#products = Product.objects.filter(category=category, subcategory=subcategory, kind=kind[0], available=True)
#products = Product.objects.filter(category=category, subcategory=subcategory, kind__in=kind, available=True)