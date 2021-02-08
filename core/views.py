import datetime

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect, reverse, redirect
from django.views.generic import FormView, TemplateView, View

from apps.dishes.models import Dish
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.tpaga.api import TpagaAPI
from common.data import (
    TERMINAL_ID,
    PURCHASE_DESCRIPTION
)
from .forms import LoginForm


tpaga = TpagaAPI()


class Login(FormView):

    template_name = "login.pug"
    form_class = LoginForm

    def get_success_url(self):
        return reverse("index")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.warning(self.request, "El usuario no se encuentra activo")
        else:
            if User.objects.filter(username=username).count() > 0:
                messages.warning(self.request, "La contraseña no es correcta")
            else:
                messages.info(self.request, "No existe el usuario")
        return HttpResponseRedirect(self.get_success_url())


class Index(LoginRequiredMixin, TemplateView):

    template_name = "index.pug"
    login_url = settings.LOGIN_URL
    permissions = {}

    def get_context_data(self, **kwargs):
        kwargs["title"] = ""
        kwargs["dishes"] = Dish.objects.all()
        return super(Index, self).get_context_data(**kwargs)


class Logout(View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_URL)


class OrderCreateView(LoginRequiredMixin, View):

    def get_order_instance(self, request, dish, count):
        order_serializer = OrderSerializer(
            data={
                "user": request.user.id,
                "dish": dish.id,
                "count": count,
                "cost": dish.amount * count,
                "terminal_id": TERMINAL_ID,
                "purchase_description": PURCHASE_DESCRIPTION,
                "purchase_items": [
                    {
                        "name": dish.name,
                        "value": dish.amount,
                        "count": count,
                    }
                ],
                "user_ip_address": request.META['REMOTE_ADDR'],
                "expires_at": datetime.datetime.now() + datetime.timedelta(minutes=5)
            }
        )

        if order_serializer.is_valid(raise_exception=True):
            order_instance = order_serializer.save()

            return order_instance

    def get_payment_request(self, request, order_instance):
        request_payment_data = {
            "cost": order_instance.cost,
            "purchase_details_url": request.build_absolute_uri(
                reverse(
                    'orders:order-detail',
                    kwargs={
                        "pk": order_instance.id.__str__()
                    }
                )
            ).replace("http", "https"),
            "voucher_url": request.build_absolute_uri(
                reverse(
                    'orders:order-detail',
                    kwargs={
                        "pk": order_instance.id.__str__()
                    }
                )
            ).replace("http", "https"),
            "idempotency_token": order_instance.idempotency_token,
            "order_id": order_instance.order_id,
            "terminal_id": order_instance.terminal_id,
            "purchase_description": order_instance.purchase_description,
            "purchase_items": order_instance.purchase_items,
            "user_ip_address": order_instance.user_ip_address,
            "expires_at": order_instance.expires_at
        }

        status_code, response_json = tpaga.create_payment_request(request_payment_data)
        return status_code, response_json

    def dispatch(self, request, *args, **kwargs):
        dish = Dish.objects.get(id=self.kwargs["pk"])
        count = int(request.GET.get("count"))

        order_instance = self.get_order_instance(request, dish, count)

        status_code, response_json = self.get_payment_request(request, order_instance)

        if status_code == 201:

            order_instance.update_attrs(response_json)

            return redirect(order_instance.tpaga_payment_url)
        return redirect("index")


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
