from urllib import request
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

from find_jobs.models import Error

from users.forms import (UserLoginForm, UserRegistrationForm, UserUpdateForm,
                         ContactForm)

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь добавлен в систему')
        return render(request, 'users/registration_done.html',
                      {'new_user': new_user})
    return render(request, 'users/registration.html', {'form': form})


def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.specialization = data['specialization']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены')
                return redirect('users:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'specialization': user.specialization,
                     'send_email': user.send_email})
        return render(request, 'users/update.html',
                    {'form': form, 'contact_form': contact_form})
    else:
        return redirect ('users:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален')
    return redirect('index')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            specialization = data.get('specialization')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'specialization': specialization})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'specialization': specialization}
                ]}
                Error(data=data).save()
            messages.success(request, 'Данные отправлены администрации')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
