from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from . import forms

from . import models


class LikeProduct(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            like = models.LikeProduct.objects.get(user_id=self.request.user.id, product_id=id)
            like.delete()
            response = 'dislike'

        except:
            models.LikeProduct.objects.create(user_id=self.request.user.id, product_id=id)
            response = 'like'

        finally:

            number_like = models.LikeProduct.objects.filter(user_id=self.request.user.id).count()
            return JsonResponse({'response': response, 'number_like': number_like})


class ProductDetailView(DetailView):
    model = models.Product
    queryset = models.Product.objects.filter(is_publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = models.Product.objects.get(slug=self.kwargs['slug']).category.all()

        related_product = models.Product.objects.filter(category__in=categories, is_publish=True).exclude(
            slug=self.kwargs['slug'])
        context['related_product'] = related_product
        context['form'] = forms.CommentProductForm()
        context['comment_product'] = models.Product.objects.get(slug=self.kwargs['slug']).comments.filter(is_publish=True).order_by('-created_at')[:5]
        return context

    def post(self, request, **kwargs):
        slug = self.kwargs['slug']
        form = forms.CommentProductForm(request.POST)

        if form.is_valid():
            product = models.Product.objects.get(slug=slug)
            message = form.cleaned_data.get('message')
            comment = models.CommentProduct.objects.create(user=self.request.user, product=product, message=message)
            comment.is_publish = True
            comment.save()
            return JsonResponse({'flag': 'True',
                                 'message': message,
                                 'url_image': request.user.image.url,
                                 'created_at': comment.created_at,
                                 'phone_user': request.user.phone,

                                 })
        return JsonResponse({'flag': 'False'})
