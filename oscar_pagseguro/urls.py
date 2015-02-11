# -*- coding: utf-8 -*-
from django.conf.urls import *

from .views import (SuccessResponseView, ReceiveNotification,
                    PagseguroRedirectView)

urlpatterns = patterns('',
    url(r'^redirect/', PagseguroRedirectView.as_view(), name='pagseguro-redirect'),
    url(r'^preview/(?P<basket_id>\d+)/$', SuccessResponseView.as_view(preview=True), name='pagseguro-success-response'),
    url(r'^checkout/payment-details/$', SuccessResponseView.as_view(preview=True), name='pagseguro-success-response'),
    url(r'^checkout/preview/$', SuccessResponseView.as_view(preview=True), name='pagseguro-success-response'),
    url(r'^retorno/pagseguro/', ReceiveNotification.as_view(), name='checkout_pagseguro_notification'),
)
