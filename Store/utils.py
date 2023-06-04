from .models import OrderItem


def recalculate_order_total(order):
    order_items = OrderItem.objects.filter(order=order)
    order.total_amount = sum(item.product.unit_price * item.quantity for item in order_items)
    order.save()
    return order



def remove_quantity_from_inventory(cart_item):
    product = cart_item.product
    quantity = cart_item.quantity

    # Update the product inventory by subtracting the quantity
    product.inventory -= quantity
    product.save()

def update_quantity_from_inventory(order_item,quantity):
    product = order_item.product
    old_quantity=order_item.quantity
    new_quantity=quantity
    diff_quantity= new_quantity - old_quantity
    product.inventory -= diff_quantity
    product.save()


