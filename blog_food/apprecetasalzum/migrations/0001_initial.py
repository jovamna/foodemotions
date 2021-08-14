# Generated by Django 3.0.1 on 2021-05-10 15:18

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='apprecetasalzum')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='apprecetasalzum.Category')),
            ],
            options={
                'verbose_name_plural': 'categorías',
                'ordering': ['-created'],
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='Título')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Descripción')),
                ('imageauthor', models.ImageField(blank=True, null=True, upload_to='apprecetasalzum', verbose_name='Imagenautor')),
                ('image', models.ImageField(blank=True, null=True, upload_to='apprecetasalzum', verbose_name='Imagen')),
                ('imagenfront', models.ImageField(blank=True, null=True, upload_to='apprecetasalzum', verbose_name='Imagenfront')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de publicación')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('titletime', models.CharField(max_length=250, null=True, verbose_name='Tiempo')),
                ('porcion', models.CharField(max_length=300, null=True, verbose_name='Porciones')),
                ('tituloperfil', models.CharField(max_length=300, null=True, verbose_name='Tituloperfil')),
                ('perfilnutricional', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Perfilnutricional')),
                ('titleingredients', models.CharField(blank=True, max_length=255, null=True, verbose_name='Titulo-Ingredientes')),
                ('ingredienone', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-uno')),
                ('ingredientwo', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-dos')),
                ('ingredienthree', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-tres')),
                ('ingredienfour', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-cuatro')),
                ('ingredienfive', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-cinco')),
                ('ingrediensix', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-seis')),
                ('ingredienseven', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-siete')),
                ('ingredieneight', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingredient-eocho')),
                ('ingrediennine', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-nueve')),
                ('ingredienten', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-diez')),
                ('ingredieneleven', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-once')),
                ('ingredientwelve', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-doce')),
                ('ingredienthirteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-trece')),
                ('ingredienfourteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-catorce')),
                ('ingredienfifteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-quince')),
                ('salsaingredients', models.CharField(blank=True, max_length=350, null=True, verbose_name='Salsaingredientes')),
                ('ingrediensixteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-dieciseis')),
                ('ingredienseventeen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-diecisiete')),
                ('ingredieneightteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-dieciocho')),
                ('ingrediennineteen', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-diecinueve')),
                ('otrosingredients', models.CharField(blank=True, max_length=350, null=True, verbose_name='Otrosingredientes')),
                ('ingredientwenty', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-veinte')),
                ('ingredientwentyone', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-veintiuno')),
                ('ingredientwentytwo', models.CharField(blank=True, max_length=350, null=True, verbose_name='Ingrediente-veintidos')),
                ('titlepreparation', models.CharField(blank=True, max_length=300, null=True, verbose_name='Titulo-Preparacion')),
                ('stepone', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasouno')),
                ('oneprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Primero')),
                ('steptwo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasodos')),
                ('twoprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Segundo')),
                ('stepthree', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasotres')),
                ('threeprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Tercero')),
                ('stepfour', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasocuatro')),
                ('fourprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Cuarto')),
                ('stepfive', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasocinco')),
                ('fiveprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Cinco')),
                ('stepsix', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasoseis')),
                ('sixprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Seis')),
                ('stepseven', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasosiete')),
                ('sevenprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Siete')),
                ('stepeight', models.CharField(blank=True, max_length=250, null=True, verbose_name='Pasoocho')),
                ('eightprepare', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Ocho')),
                ('tituloconsejos', models.CharField(blank=True, max_length=250, null=True, verbose_name='Tituloconsejos')),
                ('consejos', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Consejos')),
                ('titlenutricion', models.CharField(blank=True, max_length=250, null=True, verbose_name='Titulonutricional')),
                ('nutricional', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Informenutricional')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='apprecetasalzum.Category', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'entrada',
                'verbose_name_plural': 'entradas',
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('content', models.TextField()),
                ('publish', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='apprecetasalzum.Comment', verbose_name='replay')),
                ('postrecipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='apprecetasalzum.Recipe')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
            },
        ),
    ]
