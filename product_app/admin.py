from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_publish', 'show_image']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('name', 'slug')


@admin.register(models.VendorProduct)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ['slug', 'is_publish', 'show_image']
    list_filter = ('is_publish',)
    list_editable = ('is_publish',)
    search_fields = ('slug',)


class ImageProductAdmin(admin.StackedInline):
    model = models.ImageProduct


class InformationsProductAdmin(admin.TabularInline):
    model = models.AddInformation


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount', 'quantity', 'is_publish']
    list_filter = ('is_publish',)
    search_fields = ('name', 'slug')
    list_editable = ('discount', 'quantity', 'is_publish')
    prepopulated_fields = {'slug':('name',)}
    inlines = (ImageProductAdmin, InformationsProductAdmin)


admin.site.register(models.Size)
admin.site.register(models.Color)
admin.site.register(models.ImageProduct)
admin.site.register(models.AddInformation)
