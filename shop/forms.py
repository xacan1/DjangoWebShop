from django import forms
from django.core.exceptions import ValidationError
from shop.models import *


class SimpleForm(forms.Form):
    pass


class ProductListForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        initial = kwargs['initial']
        get_params = initial['get_params']
        min_price = initial.get('price__min', 0)
        max_price = initial.get('price__max', 0)
        self.fields['price_range_max'].widget.attrs['min'] = min_price
        self.fields['price_range_max'].widget.attrs['max'] = max_price
        self.fields['price_range_max'].widget.attrs['value'] = get_params.get(
            'price_range_max', max_price)
        self.fields['current_price'].widget.attrs['placeholder'] = get_params.get(
            'price_range_max', max_price)

    price_range_max = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-range', 'type': 'range', 'name': 'price_range_max', 'step': '100', 'onchange': 'rangePrimary.value=value'})
    )
    current_price = forms.IntegerField(
        widget=forms.TextInput(attrs={'id': 'rangePrimary', 'readonly': '', 'form': ''}),
        required=False
    )
    sorting = forms.ChoiceField(
        choices=(('price_asc', 'Сначала дешевле'), ('price_desc', 'Сначала дороже'),
                 ('alphabet_asc', 'По алфавиту А - Я'), ('alphabet_desc', 'По алфавиту Я - А'),),
        widget=forms.Select(attrs={
                            'class': 'form-control', 'id': 'selectSorting', 'form': 'filtersAttributes'}),
    )


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
