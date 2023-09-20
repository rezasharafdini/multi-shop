from django.shortcuts import render, redirect
from django.views import View
from . import forms
from django.contrib.auth import authenticate, login


class LoginView(View):

    def get(self, request):
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
                form.add_error('username','username invalid.')




        return render(request,'account_app/login.html',{'form':form})


