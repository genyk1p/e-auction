from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .form import SignUpForm, EmailConfirmForm
from .models import TemporaryUser
from django.core.mail import EmailMessage
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext


# Регистрация новоо пользователя, заполняем форму с данными, формируем инстанс временного юзера, отправляем ссылку на
# почту для ее проверки, также отправляем проверочный код на почту
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # Если форма заполнена правильно
            new_temp_user = TemporaryUser()
            new_temp_user.username = form.cleaned_data.get('username')
            new_temp_user.password = form.cleaned_data.get('password1')
            new_temp_user.email = form.cleaned_data.get('email')
            new_temp_user.first_name = form.cleaned_data.get('first_name')
            new_temp_user.last_name = form.cleaned_data.get('last_name')
            new_temp_user.save()
            token = new_temp_user.token
            # Проверочный урл не хотел формироватся по человечески, так что я его собрал из кусочков
            url = str(request.build_absolute_uri(reverse('index')) + 'accounts/email-confirm-page/' + str(token) + '/')
            s1 = gettext('To confirm registration on https://nstopboost.com/ please follow the link ')
            s2 = gettext('or enter this code ')
            s3 = gettext(' on the E-mail confirmation page. ')
            s4 = gettext('E-mail confirmation code and link will be valid for 30 minutes. ')
            s5 = gettext('Best wishes, administration of nstopboost.com')
            em = EmailMessage(
                subject=gettext('Registrations on nstopboost.com '),
                body=s1 + url + ', ' + "\n" + s2 + str(token) + s3 + "\n" + s4 + "\n" + s5,
                from_email='support@nstopboost.com',
                to=[new_temp_user.email]
            )
            em.send()
            # try:
            #     em.send()
            # except:
            #     var1 = _('Unfortunately, at the moment it is impossible to complete the registration on our website. '
            #              'Try again later or contact support.')
            #     context = {'var1': var1, 'notification_class': 'notification is-danger'}
            #     return render(request, 'catalog/standard_message.html', context)
            return redirect(reverse_lazy(enter_email_confirm_code))

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# Если пользователь захочет ввести проверочный код, а не переходить по ссылке, то этим будет заниматся эта функция.
def enter_email_confirm_code(request):
    form = EmailConfirmForm()
    if request.method == 'POST':
        form = EmailConfirmForm(request.POST)
        if form.is_valid():
            temp_user = TemporaryUser.objects.get(token=form.cleaned_data.get('token'))
            username = temp_user.username
            password = temp_user.password
            email = temp_user.email
            first_name = temp_user.first_name
            last_name = temp_user.last_name
            User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                     last_name=last_name)
            temp_user.delete()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('successful_registration')  # страница редиректа после регистрации

    content = {'form': form}
    return render(request, 'registration/enter_email_confirm_code.html', content)


# Тут проверяется если пользователь решил перейти по ссылке подтверждения имейла
def email_confirm_url(request, token):
    all_temp_user = TemporaryUser.objects.all()
    # В этом цикле мы проверяем инстансы модели временных юзеров, и удаляем все которые
    # были сделаны более чем 30 минут назад
    for i in all_temp_user:
        if timezone.now() > (i.published + timedelta(minutes=30)):
            i.delete()
    temp_user = TemporaryUser.objects.all().filter(token=token)
    if len(temp_user) == 1:
        temp_user = TemporaryUser.objects.get(token=token)
        username = temp_user.username
        password = temp_user.password
        email = temp_user.email
        first_name = temp_user.first_name
        last_name = temp_user.last_name
        User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                 last_name=last_name)
        temp_user.delete()
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('successful_registration')  # страница редиректа после регистрации
    else:
        context = {'var1': 'Invalid confirmation link'}
        return render(request, 'catalog/standard_message.html', context)

