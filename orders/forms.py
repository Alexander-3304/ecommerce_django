from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Order, OrderItem
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


# class OrderCreateForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city',)
#         # fields = '__all__'

class OrderCreateForm(forms.ModelForm):
    captcha = CaptchaField(label='Enter picture')
    class Meta:
        model = Order
        fields = (
                'first_name',
                'last_name',
                'email',
                'phone',
                'address',
                'postal_code',
                'city',
        )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('user', 'paid',)


class CustomerForm(forms.Form):
    class Meta:
        fields = (
            "email",
            "phone",
            "address",
        )

    def save(self):
        cleaned_data = self.cleaned_data
        user = cleaned_data.get("user")

        if not user:
            raise ValidationError("User is required")


class OrderRelatedCustomer(forms.Form):
    order_form = OrderForm
    customer_form = CustomerForm

