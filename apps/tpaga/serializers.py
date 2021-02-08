from rest_framework import serializers


class PaymentRequestSerializerTPAGA(serializers.Serializer):
    cost = serializers.IntegerField()
    purchase_details_url = serializers.URLField()
    voucher_url = serializers.URLField(required=False)
    idempotency_token = serializers.UUIDField()
    order_id = serializers.UUIDField()
    terminal_id = serializers.CharField(max_length=100)
    purchase_description = serializers.CharField(max_length=100)
    purchase_items = serializers.JSONField(required=False)
    user_ip_address = serializers.IPAddressField()
    expires_at = serializers.DateTimeField()
