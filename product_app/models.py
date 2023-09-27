from django.db import models
from django.utils.html import format_html
from account_app.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    image = models.ImageField(upload_to='category/images')

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subs')

    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px" >')

    show_image.short_description = 'image'


class Size(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class VendorProduct(models.Model):
    slug = models.SlugField()
    is_publish = models.BooleanField(default=False)
    image = models.ImageField(upload_to='vendor/image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    def show_image(self):
        return format_html(f'<img src="{self.image.url}" width="50px" height="50px" >')

    show_image.short_description = 'image'


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    information_short = models.CharField(max_length=70)
    additional_information = models.TextField(null=True, blank=True)
    description = models.TextField()

    price = models.PositiveSmallIntegerField()
    discount = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()

    category = models.ManyToManyField(Category, related_name='product')
    size = models.ManyToManyField(Size, related_name='product')
    color = models.ManyToManyField(Color, related_name='product')
    vendor = models.ManyToManyField(VendorProduct, related_name='product')

    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def discounted_price(self):
        return (self.price * self.discount) / 100


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='product/images', default='product/images/product.jpg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='all_images')

    def __str__(self):
        return format_html(f'<img src="{self.image.url}" width="100px" height="100px" style="margin-left:50px">')


class AddInformation(models.Model):
    description = models.CharField(max_length=150)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='informations')

    def __str__(self):
        return self.description[:50]


class LikeProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return self.user.phone + ':' + self.product.name


class CommentProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    is_publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone + ':' + self.product.name


class OfferProduct(models.Model):
    name = models.CharField(max_length=20)
    product = models.ManyToManyField(Product, related_name='offer')
    percent = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
