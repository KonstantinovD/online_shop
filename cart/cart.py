from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    # Мы запоминаем текущую сессию в атрибуте self.session (она равна сессии из запроса request.session), чтобы иметь к
    # ней доступ в других методах класса. Затем пытаемся получить данные корзины, обращаясь к
    # self.session.get(settings.CART_SESSION_ID). Если не получаем
    # объект корзины, создаем ее как пустой словарь в сессии.

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True
    # Мы используем ID товара как ключ в словаре корзины. При этом он преобразуется в строку, потому что Django
    # использует формат JSON для сериализации данных сессии, а в JSON-ключами могут быть только строки. Данные о цене
    # также преобразуются в строку, чтобы их можно было сериализовать. В конце мы вызываем метод save(), чтобы сохранить
    # сведения в сессию.   Метод save() помечает сессию как измененную
    #                      с помощью атрибута modified – "session.modified = True".
    # Так мы говорим Django о том, что редактировали данные сессии, а теперь их необходимо сохранить

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        item = None
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item
        # Для отображения списка товаров, отложенных в корзину, нужно иметь воз-
        # можность проходить в цикле по объектам Product.

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()
