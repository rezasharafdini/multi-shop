from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from product_app import models

from . import madule


class CartView(View):
    def get(self, request):
        cart = madule.Cart(request)
        return render(request, 'cart_app/cart.html', {'cart': cart})

    def post(self, request):
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        product = models.Product.objects.get(id=product_id)
        cart = madule.Cart(self.request)
        cart.add(product, size, color, quantity)

        return redirect('cart_app:cart')


class RemoveProductView(View):
    def get(self, request, name):
        cart = madule.Cart(request)
        cart.remove_product(name)
        total_cart = cart.total_cart()
        return JsonResponse({'response': 'ok', 'total_cart': total_cart})


class AddQuantityProductView(View):
    def get(self, request, name, value):
        ob = madule.Cart(request)
        ob.add_quantity(name, int(value))
        total_cart = ob.total_cart()
        total_product = ob.cart[name]['price'] * ob.cart[name]['quantity']

        return JsonResponse({'response': 'ok', 'total_cart': total_cart, 'total_product': total_product})
