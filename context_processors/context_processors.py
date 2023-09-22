from product_app.models import Category, Product

def all_category(request):
    categories = Category.objects.filter(is_publish=True)

    return {'categories':categories}



def first_product(request):
    first_product = Product.objects.all().first()

    return {'first_product':first_product}