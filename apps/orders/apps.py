from django.apps import AppConfig
from django.urls import reverse


class OrdersConfig(AppConfig):
    name = 'apps.orders'

    def ready(self):
        self.index_name = 'Ordenes'
        self.icon = 'accessibility'
        self.url = ''
        self.permisos = {}
        self.menu = [
            {
                'name': 'Mis ordenes',
                'permiso': '',
                'url': reverse('orders:orders-list'),
                'status': '',
                'other_urls': [
                    'orders:order-detail'
                ],
                'submenu': []
            }
        ]
