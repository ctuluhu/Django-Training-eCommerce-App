from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Order, OrderItem


def thanks_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thanks.html', { 'customer_order' : customer_order })


@login_required
def orders_history(request):
    if request.user.is_authenticated:
        email = str(request.user.email)
        orders_details = Order.objects.filter(email=email)
    return render(request, 'order/orders_history.html', { 'orders_details' : orders_details })


@login_required
def order_details(request, order_id):
    print(request)
    if request.user.is_authenticated:
        email = str(request.user.email)
        order = Order.objects.get(id=order_id, email=email)
        order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order/order_details.html', { 'order' : order, 'order_items' : order_items })
