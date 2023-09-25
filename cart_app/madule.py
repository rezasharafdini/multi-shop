from product_app import models


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = request.session.get('cart')
        if not cart:
            cart = request.session['cart'] = {}

        self.cart = cart

    def __iter__(self):

        for item in self.cart.values():
            item['total'] = item['price'] * item['quantity']
            item['product'] = models.Product.objects.get(id=item['ID'])
            yield item

    def name_unique(self, size, color, product_id):
        result = f'{product_id}-{size}-{color}'
        return result

    def add(self, product, size, color, quantity):
        name = self.name_unique(size, color, product.id)

        if name not in self.cart.values():
            self.cart[name] = {
                'name_unique': name, 'size': size, 'color': color,
                'ID': product.id, 'quantity': 0, 'price': product.discounted_price()
            }

        self.cart[name]['quantity'] += int(quantity)
        self.save()

    def remove_product(self, name):
        if name in self.cart:
            del self.cart[name]
            self.save()

    def add_quantity(self, name, value):
        if name in self.cart:
            self.cart[name]['quantity'] += value
            self.save()

    def total_cart(self):
        total = 0
        for item in self.cart.values():
            total += item['price'] * item['quantity']
        return total

    def number_product(self):
        return len(self.cart.values())

    def remove_cart(self):
        self.cart.clear()
        self.save()


    def save(self):
        self.session.modified = True
