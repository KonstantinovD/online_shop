from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
# Мы будем использовать эту форму для добавления товаров в корзину. Класс CartAddProductForm содержит такие поля:
# ...+ quantity – количество единиц товара (доступны значения от 1 до 20). Мы используем класс
# TypedChoiceField с параметром coerce=int, чтобы автоматически преобразовывать выбранное значение в целое число;
# ...+ update – обновить (значение True) или заменить (значение False) количество
# единиц для товара. Мы используем тип поля HiddenInput,
# чтобы пользователь не видел его в своей форме.
