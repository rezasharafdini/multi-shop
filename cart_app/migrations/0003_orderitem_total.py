# Generated by Django 4.2.5 on 2023-09-25 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_app', '0002_remove_order_email_remove_order_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='total',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]