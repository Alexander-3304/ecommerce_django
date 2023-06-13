from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    DetailView,

)
from .forms import (
    OrderCreateForm,
)

from cart.servises.cart import Cart
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import transaction
from .models import Order, OrderItem

from rest_framework import  generics, viewsets

from .serializers import OrderSerializer


# Create your views here.

def commit_handler():
    return 'Translation done'


def make_qr(pk: str, cart=None):
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('https://uzumbank.uz/ru')
    qr.make()
    img = qr.make_image(fill_color='black', black_color='white')
    order_id = pk
    img.save(f'garbage/qrs/order_{order_id}_qr.png')
    return order_id


def order_create(request):
    template_name = 'order_payment.html'
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()

            form.clean()

            if form.cleaned_data:
                order.user = request.user
                order.email = request.user.email
                order.phone = form.cleaned_data.get('phone')
                order.address = form.cleaned_data.get('address')
                order.postal_code = form.cleaned_data.get('postal_code')
                order.city = form.cleaned_data.get('city')

                save_point = transaction.savepoint()

                try:
                    order.save()
                    transaction.savepoint_commit(save_point)
                except:
                    transaction.rollback(save_point)

                transaction.commit()
                transaction.on_commit(commit_handler)
            for item in cart:
                order_item = OrderItem.objects.create(
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    order=order,
                )
            make_qr(order.pk, cart)
            cart.clear()
            return render(
                request=request, template_name=template_name, context={'order': order}
            )
    else:
        if request.user.is_authenticated:
            form = OrderCreateForm(
                initial={
                    'user': request.user.first_name,
                    'last_name': request.user.last_name,
                    'first_name': request.user.first_name,
                    'customer_id': request.user.pk,

                }
            )
        else:
            form = OrderCreateForm()

    return render(
        request, 'order_create.html', {'cart': cart, 'form': form}
    )


class OrderPayment(DetailView):
    model = Order
    template_name = 'order_payment.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderPayment, self).get_context_data(**kwargs)
        context['qr'] = self.make_qr(**kwargs)

        return context

    def make_qr(self, **kwargs):
        import qrcode

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('https://uzumbank.uz/ru')
        qr.make()
        img = qr.make_image(fill_color='black', black_color='white')
        order_id = kwargs['object'].pk
        img.save(f'garbage/qrs/order_{order_id}_qr.png')
        return order_id


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order_items'] = OrderItem.Items.order_items(kwargs['object'].pk)
        context['order'] = Order.objects.select_related('user').get(
            pk=kwargs['object'].pk
        )
        context['order_price'] = sum(
            [item.price * item.quantity for item in context['order_items']]
        )
        return context



class OrderAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderPaymentAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Если пришел правильный ответ от сервера, то  проверяем еот на правильность подтверждения платежа и, при
    отсутствии заносим в базу данных
    """

    queryset = Order.objects.all()
    serialazer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        payment = get_object_or_404(Order, pk=kwargs['pk'])
        if kwargs['paid']:
            payment.paid = True
        else:
            payment.paid = False

            payment.save()

            return self.retrive(request, *args, **kwargs)