from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver
from .models import *

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('ipn valido')
    ipn = sender
    if ipn.payment_status == 'Completed':
        ...

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('ipn invalido')
    ipn = sender
    if ipn.payment_status == 'Completed':
        ...
