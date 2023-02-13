from django import forms
from django.core.exceptions import ValidationError
from shop.models import *


class SimpleForm(forms.Form):
    pass


class ProductListForm(forms.Form):
    SORT_CHOICES=(('price_asc', 'Сначала дешевле'), ('price_desc', 'Сначала дороже'),
                 ('alphabet_asc', 'По алфавиту А - Я'), ('alphabet_desc', 'По алфавиту Я - А'),)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        initial = kwargs['initial']
        min_price = initial.get('price__min', 0)
        max_price = initial.get('price__max', 0)

        get_params = initial['get_params']
        current_price = get_params.get('price_range_max', max_price)

        self.fields['price_range_max'].widget.attrs['min'] = min_price
        self.fields['price_range_max'].widget.attrs['max'] = max_price
        self.fields['price_range_max'].widget.attrs['value'] = current_price
        self.fields['current_price'].widget.attrs['placeholder'] = current_price

        # Найду и установлю значение из кортежа сортировки по значению sorting в GET параметрах, ведь именно оно прилетело нам из прошлого запроса пользователя
        if 'sorting' in get_params:
            self.fields['sorting'].initial = [choice[0] for choice in self.SORT_CHOICES if choice[0]==get_params['sorting']]

        # Динамически создам поля атрибутов товаров, ведь сайт не знает что за товары
        for attribute, values in initial['attribute_groups'].items():
            # Создам скрытое поле только ради Label что бы отобразить имя атрибута в группировке и не создавать кастомное поле для этой формы
            self.fields[attribute] = forms.CharField(label=attribute, widget=forms.HiddenInput())

            for value in values:
                name = str(value['pk'])

                if name in get_params:
                    self.fields[name] = forms.BooleanField(label=value['string_value'], widget=forms.CheckboxInput(
                        attrs={'class': 'form-check-input', 'value': attribute, 'id': f'flexCheck{name}', 'checked': ''}), required=False)
                else:
                    self.fields[name] = forms.BooleanField(label=value['string_value'], widget=forms.CheckboxInput(
                        attrs={'class': 'form-check-input', 'value': attribute, 'id': f'flexCheck{name}'}), required=False)

    price_range_max = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-range', 'type': 'range', 'name': 'price_range_max', 'step': '100', 'onchange': 'rangePrimary.value=value'})
    )
    current_price = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'id': 'rangePrimary', 'readonly': '', 'form': ''}),
        required=False
    )
    sorting = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={
                            'class': 'form-control', 'id': 'selectSorting', 'form': 'filtersAttributes'}),
        # initial=[choice[0] for choice in SORT_CHOICES]
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
