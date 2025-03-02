"""Bag Tools imports"""
from decimal import Decimal
from django import template
from coupons.models import Coupon


# pylint: disable=locally-disabled, no-member


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(product, quantity):
    """
    Calculate the subtotal for a product.
    """
    price = product.sale_price if product.sale_price else product.price
    return price * quantity


@register.inclusion_tag('components/quantity-selector.html')
def quantity_selector(product, quantity):
    """
    Renders the quantity selector component for a product.
    """
    return {'product': product, 'quantity': quantity}


@register.filter(name='calc_discount')
def calc_discount(total, discount):
    """
    Calculate the discount amount based on the total and discount percentage.
    """
    return (total * (discount / Decimal(100))) if discount > 0 else Decimal(0)


@register.filter(name='total_after_discount')
def total_after_discount(total, discount_amount):
    """
    Calculate the total amount after applying the discount.
    """
    return total - discount_amount


@register.inclusion_tag('components/coupon-info.html')
def coupon_info(coupon, savings):
    """
    Renders the coupon information component.
    """
    return {'coupon': coupon, 'savings': savings}


@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value


@register.simple_tag
def apply_coupon(subtotal, coupon_id):
    """
    Apply a coupon to the subtotal and return the discount amount.
    """
    try:
        coupon = Coupon.objects.get(id=coupon_id)
        if coupon.is_valid():
            if coupon.discount_type == 'percentage':
                discount = (coupon.discount_value / Decimal(100)) * subtotal
            elif coupon.discount_type == 'amount':
                discount = coupon.discount_value
            return min(discount, subtotal)
    except Coupon.DoesNotExist:
        return Decimal(0)
    return Decimal(0)
