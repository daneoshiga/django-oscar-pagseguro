# -*- coding: utf-8 -*-
from oscar.core.loading import get_model
from pagseguro.signals import (notificacao_status_pago,
                               notificacao_status_cancelado)

Order = get_model('order', 'Order')


def pago(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Pago')
    order.save()


def cancelado(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Cancelado')


notificacao_status_pago.connect(pago)
notificacao_status_cancelado.connect(cancelado)
