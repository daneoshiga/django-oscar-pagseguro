==================================
Pagseguro package for django-oscar
==================================

This package provides integration between django-oscar_ and Pagseguro_

.. _django-oscar: https://github.com/tangentlabs/django-oscar
.. _Pagseguro: http://pagseguro.com.br/

It's only on early development

It depends on django_pagseguro2_ library

.. _django_pagseguro2: https://github.com/allisson/django-pagseguro2/

It works by adding the Pagseguro_ API call to the handle_successful_order
method, so it finalizes the order before redirecting the user to Pagseguro_
because it needs to use the order number as reference for the order.

Pagseguro_ assumes that the order is completed when it's called, which is
different from django-oscar, where it's possible to use the success of the
payment as a confirmation for order placement.

The payment status are sent afterwards and dealt with using a view provided by
django_pagseguro2_ library, the signals are then used for order status changing
in signals.py

Usage
-----

    pip install django-oscar-pagseguro

    - Add the pagseguro package to the INSTALLED_APPS::

        INSTALLED_APPS = [
        ...
        pagseguro,
        ]

    - Add the following url to the urls.py of the django-oscar project::

        url(r'^', include('oscar_pagseguro.urls')),

    - And have a oscar order status pipeline that matches Pagseguro one::


        OSCAR_ORDER_STATUS_PIPELINE = {
            'Aguardando pagamento': ('Paga', u'Em analíse', 'Cancelada'),
            u'Em analíse': ('Paga', 'Cancelada'),
            'Paga': ('Em disputa', 'Devolvida', u'Disponível', 'Cancelada'),
            u'Disponível': ('Devolvida', 'Em disputa'),
            'Em disputa': (u'Disponível', 'Devolvida', 'Paga'),
            'Devolvida': (),
            'Cancelada': (),
        }

TODO
----

Drop the status pipeline matching by making the status used by the
django_pagseguro2_ configurable
