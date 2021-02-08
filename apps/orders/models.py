from django.db import models
import uuid
from apps.dishes.models import Dish
from django.contrib.auth.models import User


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField()

    miniapp_user_token = models.TextField(blank=True, null=True)
    cost = models.IntegerField()
    purchase_details_url = models.URLField(blank=True, null=True)
    voucher_url = models.URLField(blank=True, null=True)
    terminal_id = models.TextField()
    purchase_description = models.TextField()
    purchase_items = models.JSONField(default=dict)
    user_ip_address = models.GenericIPAddressField()
    merchant_user_id = models.TextField(blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    tpaga_payment_url = models.URLField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()
    cancelled_at = models.TextField(blank=True, null=True)
    checked_by_merchant_at = models.TextField(blank=True, null=True)
    delivery_notification_at = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.id.__str__()

    @property
    def order_id(self):
        return self.id.__str__()

    @property
    def idempotency_token(self):
        return self.id.__str__()

    def update_attrs(self, json_dict):
        for key in json_dict:
            if hasattr(self, key) and key not in ["order_id", "idempotency_token", "cost"]:
                setattr(self, key, json_dict[key])
        self.save()

    def get_pretty_cost(self):
        return "$ {:20,.2f}".format(self.cost)
