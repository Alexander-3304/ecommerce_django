from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.CharField(label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    class Meta:
        fields = ('quantity', 'update')
        widgets = {
            'quantity': forms.TextInput(
                attrs={
                    'class': 'product_quantity_number js-number',
                    'value': 1,
                }),
            'update': forms.HiddenInput(),
        }