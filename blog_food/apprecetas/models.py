from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Kategory(MPTTModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children',
                            on_delete=models.CASCADE)
    slug = models.SlugField(
        unique=True,
        max_length=255,
        null=True,
    )
    image = models.ImageField(blank=True, null=True, upload_to="apprecetas")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Fecha de edición")

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ((
            'parent',
            'slug',
        ))
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
        return Receta.objects.filter(kategory__in=self.get_descendants(
            include_self=True)).count()


class Receta(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.TextField(max_length=400, verbose_name="Título")
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = RichTextField(null=True,
                                blank=True,
                                verbose_name="Descripción")
    imageauthor = models.ImageField(verbose_name="Imagen-autor",
                                    upload_to="apprecetas",
                                    null=True,
                                    blank=True)
    author = models.ForeignKey(User,
                               verbose_name="Autor",
                               on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Imagen",
                              upload_to="apprecetas",
                              null=True,
                              blank=True)
    imagefront = models.ImageField(verbose_name="Image-front",
                                   upload_to="apprecetas",
                                   null=True,
                                   blank=True)
    publish = models.DateTimeField(verbose_name="Fecha de publicación",
                                   default=now)
    status = models.CharField(max_length=10,
                              choices=options,
                              default='published')
    titletime = models.CharField(max_length=250,
                                 null=True,
                                 verbose_name="Tiempo")
    porcion = models.CharField(max_length=250,
                               null=True,
                               verbose_name="Porciones")
    tituloperfil = models.CharField(max_length=250,
                                    blank=True,
                                    null=True,
                                    verbose_name="Titulo-perfil-nutri")
    perfilnutricional = RichTextField(null=True,
                                      blank=True,
                                      verbose_name="Perfil-Nutricional")
    titleingredients = models.CharField(max_length=255,
                                        null=True,
                                        blank=True,
                                        verbose_name="Titulo-ingredientes")
    ingredienone = models.TextField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-uno")
    ingredientwo = models.TextField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-dos")
    ingredienthree = models.TextField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingrediente-tres")
    ingredienfour = models.TextField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-cuatro")
    ingredienfive = models.TextField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-cinco")
    ingrediensix = models.TextField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-seis")
    ingredienseven = models.TextField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingrediente-siete")
    ingredieneight = models.TextField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingrediente-ocho")
    ingrediennine = models.TextField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-nueve")
    ingredienten = models.TextField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-diez")
    ingredieneleven = models.TextField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-once")
    ingredientwelve = models.TextField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-doce")
    ingredienthirteen = models.TextField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-trece")
    ingredienfourteen = models.TextField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-catorce")
    ingredienfifteen = models.TextField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Ingrediente-quince")
    salsaingredients = models.TextField(max_length=250,
                                        null=True,
                                        blank=True,
                                        verbose_name="Salsa-ingredientes")
    ingrediensixteen = models.TextField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Ingrediente-dieciseis")
    ingredienseventeen = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-diecisiete")
    ingredieneightteen = models.TextField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-dieciocho")
    ingrediennineteen = models.TextField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-diecinueve")
    ingredientwenty = models.TextField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-veinte")
    ingredientwentyone = models.TextField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-veintiuno")
    ingredientwentytwo = models.TextField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-veintidos")
    ingredientwentythree = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veintitres")
    ingredientwentyfour = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veinticuatro")
    ingredientwentyfive = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veinticinco")
    ingredientwentysix = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veintiseis")
    otrosingredients = models.TextField(max_length=250,
                                        null=True,
                                        blank=True,
                                        verbose_name="Otros-ingredientes")
    ingredientwentyseven = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veintisiete")
    ingredientwentyeight = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veintiocho")
    ingredientwentynine = models.TextField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-veintinueve")
    ingredienthirty = models.TextField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-treinta")
    titlepreparation = models.CharField(max_length=250,
                                        null=True,
                                        blank=True,
                                        verbose_name="Titulo-Preparacion")
    stepone = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Paso-uno")
    oneprepare = RichTextField(null=True, blank=True, verbose_name="Primero")
    steptwo = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Paso-dos")
    twoprepare = RichTextField(null=True, blank=True, verbose_name="Segundo")
    stepthree = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Paso-tres")
    threeprepare = RichTextField(null=True, blank=True, verbose_name="Tercero")
    stepfour = models.CharField(max_length=250,
                                null=True,
                                blank=True,
                                verbose_name="Paso-cuatro")
    fourprepare = RichTextField(null=True, blank=True, verbose_name="Cuarto")
    stepfive = models.CharField(max_length=250,
                                null=True,
                                blank=True,
                                verbose_name="Paso-cinco")
    fiveprepare = RichTextField(null=True, blank=True, verbose_name="Cinco")
    stepsix = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Paso-seis")
    sixprepare = RichTextField(null=True, blank=True, verbose_name="Seis")
    stepseven = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Paso-siete")
    sevenprepare = RichTextField(null=True, blank=True, verbose_name="Siete")
    stepeight = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Paso-ocho")
    eightprepare = RichTextField(null=True, blank=True, verbose_name="Ocho")
    stepnine = models.CharField(max_length=250,
                                null=True,
                                blank=True,
                                verbose_name="Paso-nueve")
    nineprepare = RichTextField(null=True, blank=True, verbose_name="Nueve")
    stepten = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Paso-diez")
    tenprepare = RichTextField(null=True, blank=True, verbose_name="Diez")
    stepeleven = models.CharField(max_length=250,
                                  null=True,
                                  blank=True,
                                  verbose_name="Paso-once")
    elevenprepare = RichTextField(null=True, blank=True, verbose_name="Once")
    titulotips = models.CharField(max_length=250,
                                  null=True,
                                  blank=True,
                                  verbose_name="Titulo-tips")
    tips = RichTextField(null=True, blank=True, verbose_name="Tips")
    titlenutricion = models.CharField(max_length=250,
                                      null=True,
                                      blank=True,
                                      verbose_name="Titulo-nutricion")
    nutricional = RichTextField(null=True,
                                blank=True,
                                verbose_name="Informe-nutricional")
    kategory = TreeForeignKey(Kategory,
                              verbose_name='Categoria',
                              null=True,
                              blank=True,
                              related_name='recetas',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,
                                   verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "entrada"
        verbose_name_plural = "entradas"
        ordering = ['-publish']

    def __str__(self):
        return self.title

    #SEO
    @property
    def convert_in_meta(self):
        title = (self.title)[0:50]
        description = (self.description)[0:100]
        descripcion = title + str(description)
        return descripcion

    def get_cat_list(self):
        k = self.kategory  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('apprecetas:receta', kwargs={'slug': self.slug})

    def get_all_receta(self):
        # To display all items from all subcategories
        return Receta.objects.filter(kategory__in=self.get_descendants(
            include_self=True))


class Comment(MPTTModel):
    post = models.ForeignKey(Receta,
                             on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    class Meta:
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return 'Comment by {}'.format(self.name)
