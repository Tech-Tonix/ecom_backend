from .models import OrderItem


def recalculate_order_total(order):
    order_items = OrderItem.objects.filter(order=order)
    order.total_amount = sum(item.product.unit_price * item.quantity for item in order_items)
    order.save()
    return order
    