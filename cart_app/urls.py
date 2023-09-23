from django.urls import path
from . import views

app_name = 'cart_app'
urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('remove/product/<str:name>', views.RemoveProductView.as_view(), name='remove_product'),
    path('add/quantity/<str:name>/<str:value>', views.AddQuantityProductView.as_view(), name='add_quantity')
]
