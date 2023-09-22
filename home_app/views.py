from django.shortcuts import render
from django.views.generic import TemplateView
from product_app import models


class HomeView(TemplateView):
    template_name = 'home_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_products'] = models.Product.objects.order_by('-created_at').filter(is_publish=True)[:8]
        context['vendors'] = models.VendorProduct.objects.filter(is_publish=True)
        context['products'] = models.Product.objects.filter(is_publish=True)[:8]

        return context




