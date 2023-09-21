from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'account_app'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='Register'),
    path('check/otp', views.CheckOtp.as_view(), name='check_otp'),
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),
    path('add/address/',views.AddAddressView.as_view(), name='add_address')
]
