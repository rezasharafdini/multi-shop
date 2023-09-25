from django.db import models
from django.utils import timezone

from account_app.models import User
from product_app.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.PositiveSmallIntegerField()

    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')

    size = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    quantity = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product.name}-{self.size}-{self.color}-{self.quantity}'


class CouponCode(models.Model):
    name = models.CharField(max_length=10,unique=True)
    discount = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=False)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()


    def __str__(self):
        return self.name
