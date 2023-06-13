from django.shortcuts import render, redirect, get_object_or_404

from cart.forms import CartAddProductForm
from ustora_001.models import Item, ItemSet, Category
from django.forms.formsets import ORDERING_FIELD_NAME
from django.forms import modelformset_factory
from django.views.generic import TemplateView, ListView, DetailView
from ustora_001.forms import ItemForm, ItemImageForm


# Create your views here.

# class ItemListView(TemplateView):
#     template_name = 'site.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['items'] = Item.objects.filter(in_stock=True)
#
#         return context

class ItemListView(TemplateView):
    template_name = 'site.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.prefetch_related('images').all()

        return context

class ItemDetailView(TemplateView):
    template_name = "products_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"item": get_object_or_404(Item, in_stock=True, pk=self.kwargs["pk"])}

        return context

# class ItemDetailView(DetailView):
#     template_name = 'products_detail.html'
#     model = ItemSet
#     context_object_name = 'product_set'

class ItemCategoryView(DetailView):
    model = Category
    template_name = 'products_category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.filter(category=kwargs['object'])
        return context


# class ItemsListView(ListView):
#     model = ItemSet
#     template_name = 'products_list.html'
#     cart_product_form = CartAddProductForm()
#     context_object_name = 'products_set'

def item_detail(request, id, slug):
    product = get_object_or_404(Item, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    template_name = 'products_detail.html'
    context = {'product': product, 'cart_product_form': cart_product_form}

    return render(request, template_name=template_name, context=context)


def items_bulk_edit(request):
    ProductFormSet = modelformset_factory(
        Item, form=ItemImageForm, fields=('name', 'description', 'new_price', 'old_price', 'image'), extra=1, can_delete=True, can_order=True
    )
    template_name = 'product_bulk_edit.html'
    context = {}

    if request.method == 'POST':
        formset = ProductFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product = form.save(commit=False)
                    product.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    product.save()
            return redirect('products:products_bulk_edit')
    else:
        formset = ProductFormSet(queryset=Item.objects.all())
    context['product_form_set'] = formset
    return render(request, template_name, context)





