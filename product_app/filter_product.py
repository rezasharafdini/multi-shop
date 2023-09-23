from . import views


def filter(request, queryset):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    colors = request.GET.getlist('color')
    sizes = request.GET.getlist('size')

    sort = request.GET.get('sort')
    paginate_by = request.GET.get('paginate_by')

    search = request.GET.get('q')
    category = request.GET.get('category')

    if category:
        queryset = queryset.filter(category__name=category)
    if sort:
        if sort == 'latest':
            queryset = queryset.order_by('-created_at')

    if paginate_by:
        views.ProductListView.paginate_by = paginate_by

    else:
        views.ProductListView.paginate_by = 1

    if search:
        queryset = queryset.filter(name__icontains=search)

    if colors:
        queryset = queryset.filter(color__name__in=colors)

    if sizes:
        queryset = queryset.filter(size__name__in=sizes)

    if min_price and max_price:
        queryset = queryset.filter(price__lte=max_price, price__gte=min_price)

    return queryset
