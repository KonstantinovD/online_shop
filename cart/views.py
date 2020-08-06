from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')
# Обработчик принимает ID товара в качестве аргумента, по которому мы получаем объект Product из базы данных.
# Для работы с корзиной создаем форму CartAddProductForm и, если она валидна, добавляем или обновляем сведения о товаре.
# В конце перенаправляем пользователя на URL с названием cart_detail. По этому адресу покупатель сможет
# увидеть содержимое своей корзины.


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
