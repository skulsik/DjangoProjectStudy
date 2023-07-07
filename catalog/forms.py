from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import request

import users
from catalog.models import *



class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogCreateViewForm(FormStyleMixin, forms.ModelForm):
    bad_list_words = [
        'казино',
        'криптовалюта',
        'крипта', 'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in self.bad_list_words:
            if word in name:
                raise ValidationError('Вы использовали запрещенные слова "Казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар."')

        return name

    def clean_content(self):
        content = self.cleaned_data['content']
        for word in self.bad_list_words:
            if word in content:
                raise ValidationError('Вы использовали запрещенные слова "Казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар."')

        return content

    class Meta:
        model = Blog
        fields = ('name', 'content', 'image', 'date_of_creation')


class UserFromRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Получает пользователя """
        user = kwargs.pop('user')
        super(UserFromRequestForm, self).__init__(*args, **kwargs)
        self._user = user


class ProductCreateViewForm(UserFromRequestForm, FormStyleMixin, forms.ModelForm):
    bad_list_words = [
        'казино',
        'криптовалюта',
        'крипта', 'биржа',
        'дешево',
        'бесплатно',
        'обман',
        'полиция',
        'радар'
    ]

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in self.bad_list_words:
            if word in name:
                raise ValidationError(
                    'Вы использовали запрещенные слова "Казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар."')

        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in self.bad_list_words:
            if word in description:
                raise ValidationError(
                    'Вы использовали запрещенные слова "Казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар."')

        return description

    def __init__(self, *args, **kwargs):
        """ Если нет прав на определенное действие, просто прячем поле в форме """
        super(ProductCreateViewForm, self).__init__(*args, **kwargs)

        if not self._user.has_perm('catalog.can_deactivate_product'):
            self.fields['is_active'].widget = forms.HiddenInput()
        if not self._user.has_perm('catalog.can_description_product'):
            self.fields['description'].widget = forms.HiddenInput()
        if not self._user.has_perm('catalog.can_category_product'):
            self.fields['category'].widget = forms.HiddenInput()

    class Meta:
        model = Product
        fields = ('__all__')


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('__all__')
