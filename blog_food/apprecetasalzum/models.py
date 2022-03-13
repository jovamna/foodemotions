from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


# Create your models here.
class Category(MPTTModel):
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
    image = models.ImageField(blank=True,
                              null=True,
                              upload_to="apprecetasalzum")
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

        return ' -   '.join(full_path[::-1])

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

    def get_recursive_recipe_count(self):
        return Recipe.objects.filter(category__in=self.get_descendants(
            include_self=True)).count()


class Recipe(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=400, verbose_name="Título")
    slug = models.SlugField(max_length=255, null=True, unique=True)
    description = RichTextField(null=True,
                                blank=True,
                                verbose_name="Descripción")
    imageauthor = models.ImageField(verbose_name="Imagenautor",
                                    upload_to="apprecetasalzum",
                                    null=True,
                                    blank=True)
    author = models.ForeignKey(User,
                               verbose_name="Autor",
                               on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Imagen",
                              upload_to="apprecetasalzum",
                              null=True,
                              blank=True)
    imagenfront = models.ImageField(verbose_name="Imagenfront",
                                    upload_to="apprecetasalzum",
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
    porcion = models.CharField(max_length=300,
                               null=True,
                               verbose_name="Porciones")
    tituloperfil = models.CharField(max_length=300,
                                    null=True,
                                    verbose_name="Tituloperfil")
    perfilnutricional = RichTextField(null=True,
                                      blank=True,
                                      verbose_name="Perfilnutricional")
    titleingredients = models.CharField(max_length=255,
                                        null=True,
                                        blank=True,
                                        verbose_name="Titulo-Ingredientes")
    ingredienone = models.CharField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-uno")
    ingredientwo = models.CharField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-dos")
    ingredienthree = models.CharField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingrediente-tres")
    ingredienfour = models.CharField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-cuatro")
    ingredienfive = models.CharField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-cinco")
    ingrediensix = models.CharField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-seis")
    ingredienseven = models.CharField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingrediente-siete")
    ingredieneight = models.CharField(max_length=350,
                                      null=True,
                                      blank=True,
                                      verbose_name="Ingredient-eocho")
    ingrediennine = models.CharField(max_length=350,
                                     null=True,
                                     blank=True,
                                     verbose_name="Ingrediente-nueve")
    ingredienten = models.CharField(max_length=350,
                                    null=True,
                                    blank=True,
                                    verbose_name="Ingrediente-diez")
    ingredieneleven = models.CharField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-once")
    ingredientwelve = models.CharField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-doce")
    ingredienthirteen = models.CharField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-trece")
    ingredienfourteen = models.CharField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-catorce")
    ingredienfifteen = models.CharField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Ingrediente-quince")
    salsaingredients = models.CharField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Salsaingredientes")
    ingrediensixteen = models.CharField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Ingrediente-dieciseis")
    ingredienseventeen = models.CharField(
        max_length=350,
        null=True,
        blank=True,
        verbose_name="Ingrediente-diecisiete")
    ingredieneightteen = models.CharField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-dieciocho")
    ingrediennineteen = models.CharField(max_length=350,
                                         null=True,
                                         blank=True,
                                         verbose_name="Ingrediente-diecinueve")
    otrosingredients = models.CharField(max_length=350,
                                        null=True,
                                        blank=True,
                                        verbose_name="Otrosingredientes")
    ingredientwenty = models.CharField(max_length=350,
                                       null=True,
                                       blank=True,
                                       verbose_name="Ingrediente-veinte")
    ingredientwentyone = models.CharField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-veintiuno")
    ingredientwentytwo = models.CharField(max_length=350,
                                          null=True,
                                          blank=True,
                                          verbose_name="Ingrediente-veintidos")
    titlepreparation = models.CharField(max_length=300,
                                        null=True,
                                        blank=True,
                                        verbose_name="Titulo-Preparacion")
    stepone = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Pasouno")
    oneprepare = RichTextField(null=True, blank=True, verbose_name="Primero")
    steptwo = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Pasodos")
    twoprepare = RichTextField(null=True, blank=True, verbose_name="Segundo")
    stepthree = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Pasotres")
    threeprepare = RichTextField(null=True, blank=True, verbose_name="Tercero")
    stepfour = models.CharField(max_length=250,
                                null=True,
                                blank=True,
                                verbose_name="Pasocuatro")
    fourprepare = RichTextField(null=True, blank=True, verbose_name="Cuarto")
    stepfive = models.CharField(max_length=250,
                                null=True,
                                blank=True,
                                verbose_name="Pasocinco")
    fiveprepare = RichTextField(null=True, blank=True, verbose_name="Cinco")
    stepsix = models.CharField(max_length=250,
                               null=True,
                               blank=True,
                               verbose_name="Pasoseis")
    sixprepare = RichTextField(null=True, blank=True, verbose_name="Seis")
    stepseven = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Pasosiete")
    sevenprepare = RichTextField(null=True, blank=True, verbose_name="Siete")
    stepeight = models.CharField(max_length=250,
                                 null=True,
                                 blank=True,
                                 verbose_name="Pasoocho")
    eightprepare = RichTextField(null=True, blank=True, verbose_name="Ocho")
    tituloconsejos = models.CharField(max_length=250,
                                      null=True,
                                      blank=True,
                                      verbose_name="Tituloconsejos")
    consejos = RichTextField(null=True, blank=True, verbose_name="Consejos")
    titlenutricion = models.CharField(max_length=250,
                                      null=True,
                                      blank=True,
                                      verbose_name="Titulonutricional")
    nutricional = RichTextField(null=True,
                                blank=True,
                                verbose_name="Informenutricional")
    category = TreeForeignKey(Category,
                              verbose_name='Categoria',
                              null=True,
                              blank=True,
                              related_name='recipes',
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

    #def get_absolute_url(self):
    #return reverse('apprecetasalzum:receta', kwargs={'slug': self.slug})

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

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
        return reverse('apprecetasalzum:receta', kwargs={'slug': self.slug})


def get_all_recipe(self):
    # To display all items from all subcategories
    return Recipe.objects.filter(category__in=self.get_descendants(
        include_self=True))


class Comment(MPTTModel):
    postrecipe = models.ForeignKey(Recipe,
                                   on_delete=models.CASCADE,
                                   related_name='comments')
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            verbose_name='replay',
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
