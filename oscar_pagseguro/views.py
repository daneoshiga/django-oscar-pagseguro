# -*- coding: utf-8 -*-
from oscar.core.loading import get_class

PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')


class SuccessResponseView(PaymentDetailsView):
    pass
