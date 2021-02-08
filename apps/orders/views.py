from braces.views import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import reverse, redirect
from django.views.generic import TemplateView, View

from apps.tpaga.api import TpagaAPI
from common.data import (
    PAID_STATUS,
    DELIVERED_STATUS,
)
from core.utils import convert_dict_breadcrums
from .models import Order

tpaga = TpagaAPI()


class OrdersList(LoginRequiredMixin, TemplateView):
    template_name = 'orders/list.pug'
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):
        kwargs['title'] = 'Mis ordenes'
        kwargs['title_panel'] = 'Listado de mis ordenes'
        kwargs['breadcrumbs'] = convert_dict_breadcrums([
            ('Inicio', reverse('index')),
            ('Mis ordenes', '#'),
        ])
        kwargs['url_datatable'] = reverse('orders:rest:orders_list')
        return super(OrdersList, self).get_context_data(**kwargs)


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = "order_detail.pug"
    login_url = settings.LOGIN_URL
    permissions = {}

    def dispatch(self, request, *args, **kwargs):
        self.order = Order.objects.get(id=self.kwargs["pk"])

        status_code, response_json = tpaga.get_payment_request(self.order.token)
        if status_code == 200:
            self.order.update_attrs(response_json)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["title"] = ""
        kwargs["order"] = self.order
        return super(OrderDetailView, self).get_context_data(**kwargs)


class OrderReverseView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs["pk"])

        if order.status in [PAID_STATUS, DELIVERED_STATUS]:

            status_code, response_json = tpaga.refund_payment_request(order.token)

            if status_code == 200:

                order.update_attrs(response_json)

        return redirect("orders:orders-list")
