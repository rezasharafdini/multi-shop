from django.contrib import admin
from . import models


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'is_paid']
    list_filter = ('is_paid',)
    list_editable = ('is_paid',)
    inlines = (OrderItemAdmin,)


@admin.register(models.CouponCode)
class CouponCodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_from', 'valid_to', 'discount', 'quantity', 'active']
    list_filter = ('active',)
    list_editable = ('active', 'quantity')
