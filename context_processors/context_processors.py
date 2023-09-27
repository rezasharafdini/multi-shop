from product_app.models import Category, Product
from account_app.models import  PrimaryUserProfile

def all_category(request):
    categories = Category.objects.filter(is_publish=True)

    return {'categories': categories}


def first_product(request):
    first_product = Product.objects.all().first()

    return {'first_product': first_product}


def user_profile(request):
    main_user = PrimaryUserProfile.objects.all().first()
    return {'main_user':main_user}
