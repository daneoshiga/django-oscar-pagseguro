# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import six

from oscar.apps.payment import models
from oscar.core.loading import get_class

from pagseguro.api import PagSeguroItem, PagSeguroApi

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')


class SuccessResponseView(PaymentDetailsView):

    def handle_payment(self, order_number, total, **kwargs):
        """Handles a payment related to pagseguro"""

        source_type, __ = models.SourceType.objects.get_or_create(
            name="Pagseguro")

        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            reference=order_number)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('pre-auth', total.incl_tax)

    def handle_successful_order(self, order):
        super(SuccessResponseView, self).handle_successful_order(order)

        reference = order.number

        pagseguro_api = PagSeguroApi(reference=reference)

        for line in order.lines.all():
            item = PagSeguroItem(
                id=line.pk,
                description=line.description,
                amount='{0:.2f}'.format(line.stockrecord.price_excl_tax),
                quantity=line.quantity
            )
            pagseguro_api.add_item(item)

        data = pagseguro_api.checkout()

        return redirect(data['redirect_url'])


class ReceiveNotification(OrderPlacementMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReceiveNotification, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        notification_code = self.request.POST.get('notificationCode', None)
        notification_type = self.request.POST.get('notificationType', None)

        if notification_code and notification_type == 'transaction':
            pagseguro_api = PagSeguroApi()
            response = pagseguro_api.get_notification(notification_code)

            if response.status_code == 200:
                return HttpResponse(six.b('Notificação recebida com sucesso.'))

        return HttpResponse(six.b('Notificação inválida.'), status=400)
