from django import forms
from django.core.exceptions import ValidationError
from .models import Item, ItemImage

class ItemForm(forms.ModelForm):
    error_css_class = 'error_class'
    class Meta:
        model = Item
        fields = '__all__'


    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Цена не может быть отрицательной')

        if errors:
            raise ValidationError(errors)

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = '__all__'
