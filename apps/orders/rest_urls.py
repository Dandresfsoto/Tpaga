from django.urls import path
from .rest_views import OrdersListApi

app_name = 'rest'

urlpatterns = [
    path('', OrdersListApi.as_view(), name='orders_list'),
]
