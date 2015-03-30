# -*- coding: utf-8 -*-
from django.shortcuts import redirect

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
