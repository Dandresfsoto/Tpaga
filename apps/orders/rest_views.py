from braces.views import MultiplePermissionsRequiredMixin
from django.db.models import Q
from django_datatables_view.base_datatable_view import BaseDatatableView

from apps.orders.models import Order
from apps.utils import render_column_utils
from common.data import (
    PAID_STATUS,
    DELIVERED_STATUS,
)


class OrdersListApi(BaseDatatableView):
    model = Order
    columns = ["id", "created_at", "dish", "count", "cost", "status", "user_ip_address"]
    order_columns = ["id", "created_at", "dish", "count", "cost", "status", "user_ip_address"]

    def get_initial_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(user=self.request.user)

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            q = Q(dish__name__icontains=search) | Q(status__icontains=search)
            qs = qs.filter(q)
        return qs

    def render_column(self, row, column):
        if column == 'id':
            url = f'{row.id}'
            data_placement = 'right'
            title = f'Ver orden: {row.id}'
            return render_column_utils.edit_button(permiso=True, url=url, data_placement=data_placement, title=title)

        elif column == 'dish':
            return row.dish.name

        elif column == 'cost':
            return row.get_pretty_cost()

        if column == 'user_ip_address':
            permiso = self.request.user.is_superuser and row.status in [PAID_STATUS, DELIVERED_STATUS]
            url = f'reversar/{row.id}'
            data_placement = 'right'
            title = f'Reversar orden: {row.id}'
            return render_column_utils.delete_button(permiso=permiso, url=url, data_placement=data_placement, title=title)

        else:
            return super(OrdersListApi, self).render_column(row, column)
