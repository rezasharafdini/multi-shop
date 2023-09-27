from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from product_app import models

from django.contrib.auth.mixins import LoginRequiredMixin
from . import madule
from .models import Order, OrderItem, CouponCode

from django.conf import settings
import requests
import json


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


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/cart/verify'


def send_request(request,order_id):
    order = get_object_or_404(Order,id=order_id,user=request.user)
    order.address = request.POST.get('address_user')

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.total_price,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(request, authority):
    order_id = int(request.session['order_id'])
    order = Order.objects.get(id=order_id)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.total_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            order.is_paid = True
            order.save()
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}

    return response
