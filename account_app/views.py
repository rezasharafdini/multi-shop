import random
import uuid
import ghasedakpack

from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView

from . import forms, models
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


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

            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/')
            else:
                messages.error(request, 'username invalid')
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
            # sms = ghasedakpack.Ghasedak("Your ApiKey")
            # sms.verification({'receptor': form.cleaned_data['phone'], 'type': '1', 'template': 'randcode', 'param1': randcode})

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


class ContactUsView(LoginRequiredMixin, FormView):
    template_name = 'account_app/contact.html'
    form_class = forms.ContactUsForm
    success_url = '/'

    def form_valid(self, form):
        cd = form.cleaned_data

        if self.request.user.email:
            email = self.request.user.email
        else:
            email = cd['email']

        message = cd['message'] + '/' + email
        send_mail(cd['subject'], message, 'rezasharafdinin@gmail.com',
                  ['rezasharafdinin@gmail.com'], fail_silently=True)

        return super().form_valid(form=form)

    def form_invalid(self, form):
        form.add_error('subject', 'email is wrong')
        return self.render_to_response(self.get_context_data(form=form))


class AddAddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = forms.AddAddressForm()
        return render(request, 'account_app/checkout.html', {'form': form})

    def post(self, request):
        form = forms.AddAddressForm(request.POST)
        next_page = request.GET.get('next_page')
        if form.is_valid():
            object = form.save(commit=False)
            object.user = self.request.user
            if models.AddressUser.objects.filter(user=self.request.user).count() > 3:
                messages.error(request,'Your Address more than 4')
                return render(request, 'account_app/checkout.html', {'form': form})

            object.save()
            if next_page:
                return redirect(next_page)

            return redirect('account_app:add_address')
        form.add_error('address', 'form is wrong.')
        return render(request, 'account_app/checkout.html', {'form': form})


class EmailForLettersView(View):
    def post(self, request):
        email = request.POST.get('email')
        models.EmailForNewLetter.objects.get_or_create(email=email)
        return JsonResponse({'response': 'ok'})
