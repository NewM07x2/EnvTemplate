# Generated initial migration for sample app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('content', models.TextField(verbose_name='content')),
                ('excerpt', models.TextField(blank=True, null=True, verbose_name='excerpt')),
                ('is_published', models.BooleanField(default=False, verbose_name='is published')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='published at')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='views count')),
                ('likes_count', models.PositiveIntegerField(default=0, verbose_name='likes count')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='samples', to='sample.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'sample',
                'verbose_name_plural': 'samples',
                'ordering': ['-created_at'],
            },
        ),
    ]
