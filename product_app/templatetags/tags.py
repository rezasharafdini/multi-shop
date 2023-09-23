from product_app import models
from django import template

register = template.Library()


@register.simple_tag
def is_like(user_id, product_id):
    try:
        models.LikeProduct.objects.get(user_id=user_id, product_id=product_id)
        return True
    except:
        return False


@register.simple_tag
def number_like(user_id):
    return models.LikeProduct.objects.filter(user_id=user_id).count()


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode is not None:
        querystring = urlencode.split('&')
        queryfilter = filter(lambda p: p.split('=')[0] != field_name, querystring)
        query = '&'.join(queryfilter)
        url = '{}&{}'.format(url, query)

    return url


@register.simple_tag
def existence_variable(request, name, variable):
    lst = request.GET.getlist(name)

    if variable in lst:
        return True
    else:
        return False
