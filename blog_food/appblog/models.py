from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify




# Create your models here.
class Kategoria(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, null=True,)
    image = models.ImageField(blank=True, null=True, upload_to="appblog")
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
        for idx, ancestor in enumerate(slugs, 1):
            new_slugs.append('/'.join(slugs[:idx]))
        return new_slugs   



    def get_recursive_perderpeso_count(self):
        return Post.objects.filter(kategoria__in=self.get_descendants(include_self=True)).count()        


    
       

    #@property
    #def get_post(self):
        #return Post.objects.filter(categories__name=self.name)    


class Post(models.Model):
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=600, verbose_name="Título")
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField(max_length=1900, null= True, verbose_name="Descripción")
    publish = models.DateTimeField(verbose_name="Fecha de publicación", default=now)
    imagefront = models.ImageField(verbose_name="Imagenfront", upload_to="appblog", null=True, blank=True)
    subtitle = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo")
    content = RichTextField(null=True, blank=True, verbose_name="Contenido")
    blocquote= models.TextField(max_length =300, null=True, blank=True, verbose_name= "Blocquote")
    subtitleuno = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-uno-uno")
    narrativa = RichTextField(null=True, blank=True, verbose_name="Narrativa")
    cursiva = models.TextField(max_length=600, null=True, blank=True, verbose_name="Cursiva")
    titleone = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-uno")
    imageone = models.ImageField(verbose_name="Imagen-uno", upload_to="appblog", null=True, blank=True)
    subtitleone = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-uno")
    contenone = RichTextField(null=True, blank=True, verbose_name="Contenido-uno")
    titletwo = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-dos")
    imagetwo = models.ImageField(verbose_name="Imagen-dos", upload_to="appblog", null=True, blank=True)
    subtitletwo = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-dos")
    contentwo = RichTextField(null=True, blank=True, verbose_name="Contenido-dos")
    titlethree = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-tres")
    imagethree = models.ImageField(verbose_name="Imagen-tres", upload_to="appblog", null=True, blank=True)
    subtitlethree = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-tres")
    contenthree = RichTextField(null=True, blank=True, verbose_name="Contenido-tres")
    titlefour = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-cuatro")
    imagefour = models.ImageField(verbose_name="Imagen-cuatro", upload_to="appblog", null=True, blank=True)
    subtitlefour = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-cuatro")
    contenfour = RichTextField(null=True, blank=True, verbose_name="Contenido-cuatro")
    titlefive = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-cinco")
    imagefive = models.ImageField(verbose_name="Imagen-cinco", upload_to="appblog", null=True, blank=True)
    subtitlefive = models.TextField(max_length=500, null=True, blank=True, verbose_name="Subtitulo-cinco")
    contenfive = RichTextField(null=True, blank=True, verbose_name="Contenido-cinco")
    titleultimo = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-ultimo")
    image = models.ImageField(verbose_name="Imagen", upload_to="appblog", null=True, blank=True)
    contentultimo = RichTextField(null=True, blank=True, verbose_name="Contenido-ultimo")
    status = models.CharField(max_length=10, choices=options, default='published')
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    imageauthor = models.ImageField(verbose_name="Imagenautor", upload_to="appblog", null=True, blank=True)  
    kategoria = TreeForeignKey(Kategoria, verbose_name='Categoria', null=True, blank=True, related_name='blog', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    

    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ('-publish',)

   

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        return reverse('appblog:post', kwargs={'slug': self.slug})





class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
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