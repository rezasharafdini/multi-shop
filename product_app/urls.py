from django.urls import path
from . import views

app_name = 'product_app'
urlpatterns = [
    path('like/<int:id>', views.LikeProduct.as_view(), name='like'),
    path('detail/<str:slug>', views.ProductDetailView.as_view(), name='detail_product'),
    path('list/', views.ProductListView.as_view(), name='list_product')

]
