from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify



# Create your models here.
class Categoria(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="appperderpeso")
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


    def get_recursive_perderpeso_count(self):
        return Perderpeso.objects.filter(categoria__in=self.get_descendants(include_self=True)).count()        


    

class Perderpeso(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=600, verbose_name="Título")
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = models.TextField(max_length=1000, null= True, blank=True, verbose_name="Descripción")
    publish = models.DateTimeField(verbose_name="Fecha de publicación", default=now)
    status = models.CharField(max_length=10, choices=options, default='published')
    image = models.ImageField(verbose_name="Imagen-principal", upload_to="appperderpeso", null=True, blank=True)
    imagefront = models.ImageField(verbose_name="Imagen-frontal", upload_to="appperderpeso", null=True, blank=True)
    titleone = models.TextField(max_length=500, null=True, blank=True, verbose_name="Titulo-uno")
    contentone = RichTextField(null=True, blank=True, verbose_name="Contenido-principal")
    narrativa =models.TextField(max_length=1000, null=True, blank=True, verbose_name="Narrativa")
    cursiva = models.TextField(max_length=600, null=True, blank=True, verbose_name="Cursiva")
    imagefirstweek = models.ImageField(verbose_name="Imagen-primera-semana", upload_to="appperderpeso", null=True, blank=True)
    imageprimerweek = models.ImageField(verbose_name="Imagen-primer-semana", upload_to="appperderpeso", null=True, blank=True)
    titlefirstweek = models.CharField(max_length=300, verbose_name="Titulo-Primera-Semana", null=True, blank=True)
    contentfirstweek = RichTextField(verbose_name="Descripcion-primera-semana", null=True, blank=True)
    titlediauno = models.CharField(max_length=300, verbose_name="Titulo-dia-primero", null=True, blank=True)
    imagediauno = models.ImageField(verbose_name="Imagen-dia-primero", upload_to="appperderpeso", null=True, blank=True)
    diauno = RichTextField(verbose_name="Dia-uno", null=True, blank=True)
    titlediados = models.CharField(max_length=300, verbose_name="Titulo-dia-segundo", null=True, blank=True)
    imagediados = models.ImageField(verbose_name="Imagen-dia-segundo", upload_to="appperderpeso", null=True, blank=True)
    diados = RichTextField(null=True, blank=True, verbose_name="Dia-dos")
    titlediatres = models.CharField(max_length=300, verbose_name="Titulo-dia-tercero", null=True, blank=True)
    imagediatres = models.ImageField(verbose_name="Imagen-dia-tercer", upload_to="appperderpeso", null=True, blank=True)
    diatres = RichTextField(null=True, blank=True, verbose_name="Dia-tres")
    titlediacuatro = models.CharField(max_length=300, verbose_name="Titulo-dia-cuarto", null=True, blank=True)
    imagediacuatro = models.ImageField(verbose_name="Imagen-dia-cuarto", upload_to="appperderpeso", null=True, blank=True)
    diacuatro = RichTextField(null=True, blank=True, verbose_name="Dia-cuatro")
    titlediacinco = models.CharField(max_length=300,  verbose_name="Titulo-dia-quinto", null=True, blank=True)
    imagediacinco = models.ImageField(verbose_name="Imagen-dia-quinto", upload_to="appperderpeso", null=True, blank=True)
    diacinco = RichTextField(null=True, blank=True, verbose_name="Dia-cinco")
    titlediaseis = models.CharField(max_length=300,  verbose_name="Titulo-dia-sexto", null=True, blank=True)
    imagediaseis = models.ImageField(verbose_name="Imagen-dia-sexto", upload_to="appperderpeso", null=True, blank=True)
    diaseis = RichTextField(null=True, blank=True, verbose_name="Dia-seis")
    titlediasiete = models.CharField(max_length=300,  verbose_name="Titulo-dia-septimo", null=True, blank=True)
    imagediasiete = models.ImageField(verbose_name="Imagen-dia-septimo", upload_to="appperderpeso", null=True, blank=True)
    diasiete = RichTextField(null=True, blank=True, verbose_name="Dia-siete")
    imagetwoweek = models.ImageField(verbose_name="Imagen-segunda-semana", upload_to="appperderpeso", null=True, blank=True)
    imagedosweek = models.ImageField(verbose_name="Imagen-segunda-foto-week", upload_to="appperderpeso", null=True, blank=True)
    titlesecondweek = models.CharField(max_length=300, verbose_name="Titulo-Segunda-Semana", null=True, blank=True)
    contentwoweek = RichTextField(verbose_name="Descripcion-segunda-semana", null=True, blank=True)
    titledianocho = models.CharField(max_length=300, verbose_name="Titulo-dia-octavo", null=True, blank=True)
    imagediaocho = models.ImageField(verbose_name="Imagen-dia-ocho", upload_to="appperderpeso", null=True, blank=True)
    diaocho = RichTextField(verbose_name="Dia-ocho", null=True, blank=True)
    titledianueve = models.CharField(max_length=300, verbose_name="Titulo-dia-noveno", null=True, blank=True)
    imagedianueve = models.ImageField(verbose_name="Imagen-dia-noveno", upload_to="appperderpeso", null=True, blank=True)
    dianueve = RichTextField(null=True, blank=True, verbose_name="Dia-nueve")
    titlediadiez = models.CharField(max_length=300, verbose_name="Titulo-dia-decimo", null=True, blank=True)
    imagediadiez = models.ImageField(verbose_name="Imagen-dia-decimo", upload_to="appperderpeso", null=True, blank=True)
    diadiez = RichTextField(null=True, blank=True, verbose_name="Dia-diez")
    titlediaonce = models.CharField(max_length=300, verbose_name="Titulo-dia-once", null=True, blank=True)
    imagediaonce = models.ImageField(verbose_name="Imagen-dia-once", upload_to="appperderpeso", null=True, blank=True)
    diaonce = RichTextField(null=True, blank=True, verbose_name="Dia-once")
    titlediadoce = models.CharField(max_length=300,  verbose_name="Titulo-dia-doce", null=True, blank=True)
    imagediadoce = models.ImageField(verbose_name="Imagen-dia-doce", upload_to="appperderpeso", null=True, blank=True)
    diadoce = RichTextField(null=True, blank=True, verbose_name="Dia-doce")
    titletrece = models.CharField(max_length=300,  verbose_name="Titulo-dia-trece", null=True, blank=True)
    imagediatrece = models.ImageField(verbose_name="Imagen-dia-trece", upload_to="appperderpeso", null=True, blank=True)
    diatrece = RichTextField(null=True, blank=True, verbose_name="Dia-trece")
    titlediacatorce = models.CharField(max_length=300,  verbose_name="Titulo-dia-catorce", null=True, blank=True)
    imagediacatorce = models.ImageField(verbose_name="Imagen-dia-catorce", upload_to="appperderpeso", null=True, blank=True)
    diacatorce = RichTextField(null=True, blank=True, verbose_name="Dia-catorce")
    imagethreeweek = models.ImageField(verbose_name="Imagen-tercera-semana", upload_to="appperderpeso", null=True, blank=True)
    imagetresweek = models.ImageField(verbose_name="Imagen-tercera-foto-week", upload_to="appperderpeso", null=True, blank=True)
    titlethreeweek = models.CharField(max_length=300, verbose_name="Titulo-Tercera-Semana", null=True, blank=True)
    contenthreeweek = RichTextField(verbose_name="Descripcion-tercera-semana", null=True, blank=True)
    titlediaquince = models.CharField(max_length=300, verbose_name="Titulo-dia-quince", null=True, blank=True)
    imagediaoquince = models.ImageField(verbose_name="Imagen-dia-quince", upload_to="appperderpeso", null=True, blank=True)
    diaquince = RichTextField(verbose_name="Dia-quince", null=True, blank=True)
    titlediadieciseis = models.CharField(max_length=300, verbose_name="Titulo-dia-dieciseis", null=True, blank=True)
    imagediadieciseis = models.ImageField(verbose_name="Imagen-dia-dieciseis", upload_to="appperderpeso", null=True, blank=True)
    diadieciseis = RichTextField(null=True, blank=True, verbose_name="Dia-dieciseis")
    titlediecisiete = models.CharField(max_length=300, verbose_name="Titulo-dia-diecisiete", null=True, blank=True)
    imagediadiecisiete = models.ImageField(verbose_name="Imagen-dia-diecisiete", upload_to="appperderpeso", null=True, blank=True)
    diadiecisiete = RichTextField(null=True, blank=True, verbose_name="Dia-diecisiete")
    titlediadieciocho = models.CharField(max_length=300, verbose_name="Titulo-dia-dieciocho", null=True, blank=True)
    imagediadieciocho = models.ImageField(verbose_name="Imagen-dia-dieciocho", upload_to="appperderpeso", null=True, blank=True)
    diadieciocho = RichTextField(null=True, blank=True, verbose_name="Dia-dieciocho")
    titlediadiecinueve = models.CharField(max_length=300, verbose_name="Titulo-dia-diecinueve", null=True, blank=True)
    imagediadiecinueve = models.ImageField(verbose_name="Imagen-dia-diecinueve", upload_to="appperderpeso", null=True, blank=True)
    diadiecinueve = RichTextField(null=True, blank=True, verbose_name="Dia-diecinueve")
    titlediaveinte = models.CharField(max_length=300,  verbose_name="Titulo-dia-veinte", null=True, blank=True)
    imagediaveinte = models.ImageField(verbose_name="Imagen-dia-veinte", upload_to="appperderpeso", null=True, blank=True)
    diaveinte = RichTextField(null=True, blank=True, verbose_name="Dia-veinte")
    titlediaveinteiuno = models.CharField(max_length=300,  verbose_name="Titulo-dia-veintiuno", null=True, blank=True)
    imagediaveinteiuno = models.ImageField(verbose_name="Imagen-dia-veintiuno", upload_to="appperderpeso", null=True, blank=True)
    diaveinteiuno = RichTextField(null=True, blank=True, verbose_name="Dia-veintiuno")
    imagefourweek = models.ImageField(verbose_name="Imagen-cuarto-semana", upload_to="appperderpeso", null=True, blank=True)
    imagecuatroweek = models.ImageField(verbose_name="Imagen-cuatro-foto-week", upload_to="appperderpeso", null=True, blank=True)
    titlefourweek = models.CharField(max_length=300, verbose_name="Titulo-Cuarta-Semana", null=True, blank=True)
    contenfourweek = RichTextField(verbose_name="Descripcion-cuarta-semana", null=True, blank=True)
    titlediaveintidos =models.CharField(max_length=300, verbose_name="Titulo-dia-veintidos", null=True, blank=True)
    imagediaveintidos = models.ImageField(verbose_name="Imagen-dia-veintidos", upload_to="appperderpeso", null=True, blank=True)
    diaveintidos = RichTextField( null=True, blank=True, verbose_name="Dia-veintidos")
    titlediaveintitres = models.CharField(max_length=300, verbose_name="Titulo-dia-veintitres", null=True, blank=True)
    imagediaveintitres = models.ImageField(verbose_name="Imagen-dia-veintitres", upload_to="appperderpeso", null=True, blank=True)
    diaveintitres = RichTextField(null=True, blank=True, verbose_name="Dia-veintitres")
    titlediaveinticuatro = models.CharField(max_length=300, verbose_name="Titulo-dia-veinticuatro", null=True, blank=True)
    imagediaveinticuatro = models.ImageField(verbose_name="Imagen-dia-veinticuatro", upload_to="appperderpeso", null=True, blank=True)
    diaveinticuatro = RichTextField(null=True, blank=True, verbose_name="Dia-veinticuatro")
    titlediaveinticinco = models.CharField(max_length=300, verbose_name="Titulo-dia-veinticinco", null=True, blank=True)
    imagediaveinticinco = models.ImageField(verbose_name="Imagen-dia-veinticinco", upload_to="appperderpeso", null=True, blank=True)
    diaveinticinco = RichTextField(null=True, blank=True, verbose_name="Dia-veinticinco")
    titlediaveintiseis = models.CharField(max_length=300, verbose_name="Titulo-dia-veintiseis", null=True, blank=True)
    imagediaveintiseis = models.ImageField(verbose_name="Imagen-dia-veintiseis", upload_to="appperderpeso", null=True, blank=True)
    diaveintiseis = RichTextField(null=True, blank=True, verbose_name="Dia-veintiseis")
    titlediaveintisiete = models.CharField(max_length=300, verbose_name="Titulo-dia-veintisiete", null=True, blank=True)
    imagediaveintisiete = models.ImageField(verbose_name="Imagen-dia-veintisiete", upload_to="appperderpeso", null=True, blank=True)
    diaveintisiete = RichTextField(null=True, blank=True, verbose_name="Dia-veintisiete")
    titlediaveintiocho = models.CharField(max_length=300, verbose_name="Titulo-dia-veintiocho", null=True, blank=True)
    imagediaveintiocho = models.ImageField(verbose_name="Imagen-dia-veintiocho", upload_to="appperderpeso", null=True, blank=True)
    diaveintiocho = RichTextField(null=True, blank=True, verbose_name="Dia-veintiocho")
    titlefin= models.CharField(max_length=300,  verbose_name="Titulo-conclusiones", null=True, blank=True)
    contentfin= models.TextField(max_length=1000, verbose_name="Conclusiones", null=True, blank=True,)
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE)
    categoria = TreeForeignKey(Categoria, verbose_name='Categoria', null=True, blank=True, related_name='perderpeso', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
       


    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ['-publish']

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
        return reverse('appperderpeso:post', kwargs={'slug': self.slug})        


def get_all_perderpesos(self):
        # To display all items from all subcategories
        return Perderpeso.objects.filter(category__in=self.get_descendants(include_self=True))



























