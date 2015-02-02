# -*- coding: utf-8 -*-
from oscar.apps.payment.exceptions import RedirectRequired
from oscar.core.loading import get_class

from pagseguro.api import PagSeguroItem, PagSeguroApi

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')


class SuccessResponseView(PaymentDetailsView):

    def handle_payment(self, order_number, total, **kwargs):
        """Handles a payment related to pagseguro"""

        pagseguro_api = PagSeguroApi(reference=order_number)

        basket = self.request.basket

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

        self.request.session['checkout_order_id'] = order_number

        raise RedirectRequired(url=data['redirect_url'])
