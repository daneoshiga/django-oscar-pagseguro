# -*- coding: utf-8 -*-
from oscar.core.loading import get_model
from pagseguro import signals

Order = get_model('order', 'Order')


def aguardando(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Aguardando pagamento')
    order.save()


def em_analise(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status(u'Em analíse')
    order.save()


def pago(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Paga')
    order.save()


def disponivel(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status(u'Disponível')
    order.save()


def em_disputa(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Em disputa')
    order.save()


def devolvido(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Devolvida')
    order.save()


def cancelado(sender, transaction, **kwargs):
    order = Order.objects.get(number=transaction['reference'])
    order.set_status('Cancelada')


signals.notificacao_status_aguardando.connect(aguardando)
signals.notificacao_status_em_analise.connect(em_analise)
signals.notificacao_status_pago.connect(pago)
signals.notificacao_status_disponivel.connect(disponivel)
signals.notificacao_status_em_disputa.connect(em_disputa)
signals.notificacao_status_devolvido.connect(devolvido)
signals.notificacao_status_cancelado.connect(cancelado)
