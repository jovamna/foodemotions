# Generated by Django 3.0.1 on 2021-03-29 15:24

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
            name='Categori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='appturismo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='appturismo.Categori')),
            ],
            options={
                'verbose_name_plural': 'categorías',
                'ordering': ['-created'],
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Posturismo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=600, verbose_name='Título')),
                ('slug', models.SlugField(max_length=255, null=True, unique=True)),
                ('description', models.TextField(max_length=700, null=True, verbose_name='Descripción')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de publicación')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagen')),
                ('imagefront', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagenfront')),
                ('titleone', models.TextField(blank=True, max_length=500, null=True, verbose_name='titulouno')),
                ('contentone', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenidouno')),
                ('cursiva', models.TextField(blank=True, max_length=600, null=True, verbose_name='Cursiva')),
                ('narrativa', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('imageone', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagenuno')),
                ('imagetwo', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagendos')),
                ('blocquote', models.TextField(blank=True, max_length=300, null=True, verbose_name='blocquote')),
                ('imagepic', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagendibujo')),
                ('titletwo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Titulodos')),
                ('contentwo', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenidodos')),
                ('imagethree', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagentres')),
                ('titlethree', models.CharField(blank=True, max_length=300, null=True, verbose_name='Titulotres')),
                ('contenthree', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenidotres')),
                ('imageauthor', models.ImageField(blank=True, null=True, upload_to='appturismo', verbose_name='Imagenautor')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('categori', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posturismo', to='appturismo.Categori', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'entrada',
                'verbose_name_plural': 'entradas',
                'ordering': ('-publish',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('content', models.TextField()),
                ('publish', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='appturismo.Comment')),
                ('posturismo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='appturismo.Posturismo')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
            },
        ),
    ]
