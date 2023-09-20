# Generated by Django 4.2.5 on 2023-09-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address'),
        ),
    ]
