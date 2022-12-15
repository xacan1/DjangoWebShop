from django import forms
from django.core.exceptions import ValidationError
from shop.models import *


class SimpleForm(forms.Form):
    pass


class AddOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['payment_type'].empty_label = 'Не выбран вид оплаты'
        self.fields['delivery_type'].empty_label = 'Не выбран способ получения'

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if len(phone) != 11 or not phone.isdigit() or phone[0] != '7':
            raise ValidationError('Введите правильный мобильный номер')

        return phone

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address',
                  'comment', 'delivery_type', 'payment_type', 'coupon',]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.TextInput(attrs={'placeholder': 'Электронная почта'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Пример: 79001234567'}),
            'address': forms.TextInput(attrs={'placeholder': 'Пример: Уфа, ул. Ленина, дом 1'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'delivery_type': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }
