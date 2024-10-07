"""Signals file imports"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem

# pylint: disable=unused-argument


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """

    instance.order.get_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """

    instance.order.get_total()
