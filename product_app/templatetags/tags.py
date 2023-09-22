from product_app import models
from  django import template

register = template.Library()


@register.simple_tag
def is_like(user_id,product_id):
    try:
        models.LikeProduct.objects.get(user_id=user_id, product_id=product_id)
        return True
    except:
        return False



@register.simple_tag
def number_like(user_id):
        return models.LikeProduct.objects.filter(user_id=user_id).count()
