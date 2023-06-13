from django.urls import path
from orders.views import order_create, OrderPayment, OrderDetailView, OrderAPIView, OrderPaymentAPIView

from rest_framework.routers import DefaultRouter

app_name = 'orders'

router = DefaultRouter()
router.register('payment', OrderAPIView, basename='payment')


urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('<int:pk>/qr/', OrderPayment.as_view(), name='order_qr'),
    path('<int:pk>/detail/', OrderDetailView.as_view(), name='order_detail'),

    path('<int:pk>/paid/<int:paid>/', OrderPaymentAPIView.as_view(), name='paid'),
]

urlpatterns += router.urls