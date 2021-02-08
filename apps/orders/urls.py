from django.urls import path, include
from .views import OrdersList, OrderDetailView, OrderReverseView

app_name = 'orders'

urlpatterns = [

    path('', OrdersList.as_view(), name='orders-list'),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("reversar/<uuid:pk>/", OrderReverseView.as_view(), name="order-reverse"),

    path('api/v1.0/', include('apps.orders.rest_urls', namespace='api_orders')),

]
