from django.urls import path
from ustora_001.views import ItemListView, ItemDetailView, items_bulk_edit, ItemCategoryView



app_name = 'ustora_001'



urlpatterns = [
    path('', ItemListView.as_view(), name="products_view"),
    path('<int:pk>/', ItemDetailView.as_view(), name="items_detail_view"),

    path('category/<int:pk>', ItemCategoryView.as_view(), name='items_category_view'),

    path('items_bulk_edit/', items_bulk_edit, name='items_bulk_edit'),





]




