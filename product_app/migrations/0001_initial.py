# Generated by Django 4.2.5 on 2023-09-21 08:12

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
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to='category/images')),
                ('is_publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='product_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='VendorProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('is_publish', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='vendor/image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('information_short', models.CharField(max_length=70)),
                ('additional_information', models.TextField(blank=True, null=True)),
                ('description', models.TextField()),
                ('price', models.PositiveSmallIntegerField()),
                ('discount', models.PositiveSmallIntegerField()),
                ('quantity', models.PositiveSmallIntegerField()),
                ('is_publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(related_name='product', to='product_app.category')),
                ('color', models.ManyToManyField(related_name='product', to='product_app.color')),
                ('like', models.ManyToManyField(related_name='product', to=settings.AUTH_USER_MODEL)),
                ('size', models.ManyToManyField(related_name='product', to='product_app.size')),
                ('vendor', models.ManyToManyField(related_name='product', to='product_app.vendorproduct')),
            ],
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='product/images/product.jpg', upload_to='product/images')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_images', to='product_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='AddInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='informations', to='product_app.product')),
            ],
        ),
    ]
