import random
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms, models
from django.contrib.auth import authenticate, login


class LoginView(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = forms.LoginForm()
        return render(request, 'account_app/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('username', 'username invalid.')
        return render(request, 'account_app/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):

        if self.request.user.is_authenticated:
            return redirect('/')
        form = forms.RegisterForm()
        return render(request, 'account_app/register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)

        if form.is_valid():
            token = str(uuid.uuid4())
            randcode = random.randint(10000, 99999)
            print(randcode)
            models.Otp.objects.create(phone=form.cleaned_data.get('phone'), token=token, randcode=randcode)
            self.request.session['token'] = token
            return redirect('account_app:check_otp')

        return render(request, 'account_app/register.html', {'form': form})


class CheckOtp(View):

    def get(self, request):

        form = forms.CheckOtp()
        return render(request, 'account_app/checkotp.html', {'form': form})

    def post(self, request):
        form = forms.CheckOtp(request.POST)
        token = self.request.session.get('token')

        if token:
            if form.is_valid():
                code = form.cleaned_data.get('randcode')
                otp = get_object_or_404(models.Otp, token=token, randcode=code)
                user, is_admin = models.User.objects.get_or_create(phone=otp.phone)
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                self.request.session['token'] = None
                otp.delete()
                return redirect('/')
            form.add_error('randcode', 'code is wrong.')
            return render(request, 'account_app/checkotp.html', {'form': form})

        else:
            return redirect('/')
