from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
import stripe

from .models import Cart, CartItem
from order.models import Order, OrderItem
from shop.models import Product


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return cart


def cart_add(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
        
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'eCommerce Training Site - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billing_name = request.POST['stripeBillingName']
            billing_address = request.POST['stripeBillingAddressLine1']
            billing_city = request.POST['stripeBillingAddressCity']
            billing_postcode = request.POST['stripeBillingAddressZip']
            billing_country = request.POST['stripeBillingAddressCountryCode']
            shipping_name = request.POST['stripeShippingName']
            shipping_address = request.POST['stripeShippingAddressLine1']
            shipping_city = request.POST['stripeShippingAddressCity']
            shipping_postcode = request.POST['stripeShippingAddressZip']
            shipping_country = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(email=email, source=token)
            charge = stripe.Charge.create(amount=stripe_total, currency='usd', description=description, customer=customer.id)
            '''Create the order'''
            try:
                order_details = Order.objects.create(
                    token = token,
                    total = total,
                    email = email,
                    billing_name = billing_name,
                    billing_address = billing_address,
                    billing_city = billing_city,
                    billing_postcode = billing_postcode,
                    billing_country = billing_country,
                    shipping_name = shipping_name,
                    shipping_address = shipping_address,
                    shipping_city = shipping_city,
                    shipping_postcode = shipping_postcode,
                    shipping_country = shipping_country,
                )
                order_details.save()
                for cart_item in cart_items:
                    order_item = OrderItem.objects.create(
                        product = cart_item.product.name,
                        quantity = cart_item.quantity,
                        price = cart_item.product.price,
                        order = order_details,
                    )
                    order_item.save()

                    '''Reduce stock and delete a product from the cart'''
                    products = Product.objects.get(id=cart_item.product.id)
                    products.stock = int(cart_item.product.stock - cart_item.quantity)
                    products.save()
                    cart_item.delete()

                try:
                    send_email(order_details.id)
                except IOError as e:
                    return e

                return redirect('order:thanks_page', order_details.id)
            except ObjectDoesNotExist:
                pass
        except stripe.error.CardError as e:
            return False, e

    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter, 
                                             data_key = data_key, stripe_total = stripe_total, description = description))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_detail')


def cart_delete(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()

    return redirect('cart:cart_detail')


def send_email(order_id):
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)
    try:
        subject = 'eCommerce Training Site - New Order #{}'.format(transaction.id)
        to = ['{}'.format(transaction.email)]
        order_information = {
            'transaction' : transaction,
            'order_items' : order_items,
        }
        message = get_template('email/email.html').render(order_information)
        msg = EmailMessage(subject, message, to=to)
        msg.content_subtype = 'html'
        msg.send()
    except IOError as e:
        return e
