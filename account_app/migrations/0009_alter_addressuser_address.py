# Generated by Django 4.2.5 on 2023-09-24 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0008_alter_addressuser_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressuser',
            name='address',
            field=models.CharField(max_length=300),
        ),
    ]