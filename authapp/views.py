from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm,UserProfileEditForm
from authapp.forms import ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import ShopUser
from django.db import transaction


def login(request):
    title = 'вход'
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password, backend='django.contrib.auth.backends.ModelBackend')
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:

                return HttpResponseRedirect(reverse('index'))

    content = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@transaction.atomic()
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    content = {'title': title, 'edit_form': edit_form,'profile_form':profile_form}

    return render(request, 'authapp/edit.html', content)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                return render(request, 'authapp/sent_email.html')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портал\
    {settings.DOMAIN_NAME} перейдите по ссылке:\
    \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired:
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save(update_fields=['activation_key', 'activation_key_expires', 'is_active'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')

    except Exception as e:
        pass

    else:
        return HttpResponseRedirect(reverse('index'))
