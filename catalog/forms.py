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


class ProductCreateViewForm(FormStyleMixin, forms.ModelForm):
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

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price', 'date_of_creation', 'date_of_change')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['user'] = User.objects().user
    #     print(user)


class VersionForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('__all__')
