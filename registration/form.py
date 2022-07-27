from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import TemporaryUser
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Форма регистрации нового пользователя.
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


# Форма проверки токена сгенерированого пр проверке имейла пользователя.
class EmailConfirmForm(forms.Form):
    token = forms.UUIDField(
        required=True,
        label=_('Please enter email confirmation code'),
    )
    # Проверка кода у нас выполнена по средствам валидатора, так как токен уникальный,
    # в случае совпадения должен вернутся инстас модели с длинной 1 если чтото другое вернулось,
    # значит токен не верный и форма не валидка
    def clean_token(self):
        all_temp_user = TemporaryUser.objects.all()
        token = self.cleaned_data['token']
        # В этом цикле мы проверяем инстансы модели временных юзеров, и удаляем все которые
        # были сделаны более чем 30 минут назад
        for i in all_temp_user:
            if timezone.now() > (i.published + timedelta(minutes=30)):
                i.delete()
        temp_user = TemporaryUser.objects.all().filter(token=token)
        if len(temp_user) != 1:
            raise ValidationError(_('Invalid confirmation code'))
        return token
