from typing import Dict, Tuple
import requests
from django.conf import settings
from json.decoder import JSONDecodeError
from .serializers import PaymentRequestSerializerTPAGA
import json
from common.encoders import StrEncoder


class TpagaAPI:
    base_url = "https://stag.wallet.tpaga.co/"

    def create_payment_request(self, data: Dict) -> Tuple:
        new_request_path = "merchants/api/v1/payment_requests/create/"

        payment_request_serializer = PaymentRequestSerializerTPAGA(data=data)

        if payment_request_serializer.is_valid(raise_exception=True):

            json_data = json.loads(
                json.dumps(
                    payment_request_serializer.validated_data,
                    cls=StrEncoder
                )
            )

            response = requests.post(
                url=f"{self.base_url}{new_request_path}",
                json=json_data,
                headers={"Authorization": f"Basic {settings.TPAGA_SECRET_KEY}"}
            )

            try:
                response_json = response.json()
            except JSONDecodeError:
                response_json = {}

            return response.status_code, response_json

    def get_payment_request(self, token: str) -> Tuple:
        get_request_path = f"/merchants/api/v1/payment_requests/{token}/info"

        response = requests.get(
            url=f"{self.base_url}{get_request_path}",
            headers={"Authorization": f"Basic {settings.TPAGA_SECRET_KEY}"}
        )

        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = {}

        return response.status_code, response_json

    def refund_payment_request(self, token: str) -> Tuple:
        refund_payment_path = "/merchants/api/v1/payment_requests/refund"

        response = requests.post(
            url=f"{self.base_url}{refund_payment_path}",
            json={
                "payment_request_token": token
            },
            headers={"Authorization": f"Basic {settings.TPAGA_SECRET_KEY}"}
        )

        try:
            response_json = response.json()
        except JSONDecodeError:
            response_json = {}

        return response.status_code, response_json
