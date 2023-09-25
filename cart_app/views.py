from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from product_app import models
from django.contrib.auth.mixins import LoginRequiredMixin
from . import madule
from .models import Order, OrderItem, CouponCode


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
        len_cart = cart.number_product()
        return JsonResponse({'response': 'ok', 'total_cart': total_cart, 'len_cart': len_cart})


class AddQuantityProductView(View):
    def get(self, request, name, value):
        ob = madule.Cart(request)
        ob.add_quantity(name, int(value))
        total_cart = ob.total_cart()
        total_product = ob.cart[name]['price'] * ob.cart[name]['quantity']

        return JsonResponse({'response': 'ok', 'total_cart': total_cart, 'total_product': total_product})


class OrderDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        order = Order.objects.get(id=id)
        return render(request, 'cart_app/order.html', {'order': order})


class OrderCreationView(LoginRequiredMixin, View):
    def get(self, request):
        cart = madule.Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.total_cart())

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], size=item['size'], color=item['color'],
                                     quantity=item['quantity'], total=item['total'])
        cart.remove_cart()
        return redirect('cart_app:order_detail', order.id)


class CouponView(View):

    def post(self, request, id):

        try:
            name = request.POST.get('coupon')
            order = Order.objects.get(id=id)
            now = timezone.now()
            print(now)
            coupon = CouponCode.objects.get(name=name, active=True, valid_to__gte=now, valid_from__lte=now)
            if coupon.quantity == 0:

                return JsonResponse({'flag': 'False'})
            coupon.quantity -= 1
            total = order.total_price - (order.total_price * coupon.discount) / 100
            order.total_price = total
            coupon.save()
            order.save()
            return JsonResponse({'flag': 'True', 'total': total})
        except:

            return JsonResponse({'flag': 'False'})
