from decimal import Decimal
from django.conf import settings
from ustora_001.models import Item, Category, ItemSet


class Cart(object):
    def __init__(self, request) -> None:

        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:

            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "new_price": str(product.new_price)}

        if update_quantity:
            self.cart[product_id]["quantity"] = int(quantity)
        else:
            self.cart[product_id]["quantity"] += int(quantity)

        self.save()

    def save(self):

        self.session[settings.CART_SESSION_ID] = self.cart

        self.session.modified = True

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):

        product_ids = self.cart.keys()

        products = Item.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.pk)]["product"] = product

        for p_item in self.cart.values():
            p_item["price"] = Decimal(p_item["new_price"])
            p_item["total_price"] = p_item["price"] * p_item["quantity"]
            yield p_item

    def __len__(self):

        return sum(p_item["quantity"] for p_item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(p_item["price"]) * p_item["quantity"] for p_item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
