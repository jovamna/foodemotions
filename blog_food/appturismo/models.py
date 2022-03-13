from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify




# Create your models here.
class Categori(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="appturismo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")


    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = "categorías"
        ordering = ['-created']


    def __str__(self):
        return self.name

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' - Subcategoria   '.join(full_path[::-1])


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



    def get_slug_list(self):
        ancestors = self.get_ancestors(include_self=True)
        slugs = [ancestor.slug for ancestor in ancestors]
        new_slugs = []
        for idx, ancestors in enumerate(slugs, 1):
            new_slugs.append('/'.join(slugs[:idx]))
        return new_slugs   



    def get_recursive_posturismo_count(self):
        return Posturismo.objects.filter(categori__in=self.get_descendants(include_self=True)).count()        


    #def get_all_perderpeso(self):
        #return Perderpeso.objects.filter(category__in=Category.objects.get_descendant(include_self=True))
       

    @property
    def get_post(self):
        return Posturismo.objects.filter(categories__name=self.name)    


class Posturismo(models.Model):
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=600, verbose_name="Título")
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField(max_length=700, null= True, verbose_name="Descripción")
    publish = models.DateTimeField(verbose_name="Fecha de publicación", default=now)
    status = models.CharField(max_length=10, choices=options, default='published')
    image = models.ImageField(verbose_name="Imagen", upload_to="appturismo", null=True, blank=True)
    imagefront = models.ImageField(verbose_name="Imagenfront", upload_to="appturismo", null=True, blank=True)
    contentone = RichTextField(null=True, blank=True, verbose_name="Contenido-uno")
    cursiva = models.TextField(max_length=600, null=True,  blank=True, verbose_name="Cursiva")
    titleone = models.TextField(max_length=500, null=True, blank=True, verbose_name="titulo-uno")
    imageone = models.ImageField(verbose_name="Imagen-uno", upload_to="appturismo", null=True, blank=True)
    narrativa = RichTextField(null=True, blank=True, verbose_name="Contenido-Narrativa")
    blocquote= models.TextField(max_length =300, null = True, blank=True, verbose_name= "blocquote" )
    titletwo = models.CharField(max_length=200, null=True, blank=True, verbose_name="Titulo-dos")
    imagetwo = models.ImageField(verbose_name="Imagen-dos", upload_to="appturismo", null=True, blank=True)
    contentwo = RichTextField(null=True, blank=True, verbose_name="Contenido-dos")
    titlethree = models.CharField(max_length=300, null=True, blank=True, verbose_name="Titulo-tres")
    imagethree = models.ImageField(verbose_name="Imagen-tres", upload_to="appturismo", null=True, blank=True)
    contenthree = RichTextField(null=True, blank=True, verbose_name="Contenido-tres")
    imagepic = models.ImageField(verbose_name="Imagen-dibujo", upload_to="appturismo", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    imageauthor = models.ImageField(verbose_name="Imagenautor", upload_to="appturismo", null=True, blank=True)  
    categori = TreeForeignKey(Categori, verbose_name='Categoria', null=True, blank=True, related_name='posturismo', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    

    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ('-publish',)
       

    def __str__(self):
        return self.title

    


    def get_cat_list(self):
        k = self.categoria # for now ignore this instance method
        
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('appturismo:post', kwargs={'slug': self.slug})        


    def get_all_posturismo(self):
        # To display all items from all subcategories
        return Posturismo.objects.filter(categori__in=self.get_descendants(include_self=True))








class Comment(MPTTModel):
    posturismo = models.ForeignKey(Posturismo, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=200, blank=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    class MPTTMeta:
        order_insertion_by = ['publish']

    class Meta:
        ordering=['tree_id','lft']

    def __str__(self):
        return 'Comment by {}'.format(self.name)