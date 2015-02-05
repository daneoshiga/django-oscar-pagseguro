# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import RedirectView, View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import six

from oscar.apps.payment import models
from oscar.apps.payment.exceptions import RedirectRequired
from oscar.core.loading import get_class

from pagseguro.api import PagSeguroItem, PagSeguroApi

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')
CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')


class PagseguroRedirectView(CheckoutSessionMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        basket = self.request.basket
        pagseguro_api = PagSeguroApi(reference=basket.id)

        import ipdb
        ipdb.set_trace()

        # TODO: add the options selected on description

        for line in basket.all_lines():
            item = PagSeguroItem(
                id=line.pk,
                description=line.description,
                amount='{0:.2f}'.format(line.stockrecord.price_excl_tax),
                quantity=line.quantity
            )
            pagseguro_api.add_item(item)

        data = pagseguro_api.checkout()

        return data['redirect_url']


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


class ReceiveNotification(OrderPlacementMixin, View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ReceiveNotification, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        import ipdb
        ipdb.set_trace()
        notification_code = self.request.POST.get('notificationCode', None)
        notification_type = self.request.POST.get('notificationType', None)

        if notification_code and notification_type == 'transaction':
            pagseguro_api = PagSeguroApi()
            response = pagseguro_api.get_notification(notification_code)

            if response.status_code == 200:
                return HttpResponse(six.b('Notificação recebida com sucesso.'))

        return HttpResponse(six.b('Notificação inválida.'), status=400)
