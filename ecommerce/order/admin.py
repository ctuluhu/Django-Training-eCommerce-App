from django.contrib import admin

from .models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        ('Product', { 'fields': ['product'], }),
        ('Quantity', { 'fields': ['quantity'], }),
        ('Price', { 'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    max_num = 0
    template = 'admin/order/tabular.html'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_name', 'email', 'created']
    list_display_links = ('id', 'billing_name')
    search_fields = ['id', 'billing_name', 'email']
    readonly_fields = ['id', 'token', 'total', 'email', 'created', 'billing_name', 'billing_address', 'billing_city', 'billing_postcode',
                       'billing_country', 'shipping_name', 'shipping_address', 'shipping_city', 'shipping_postcode', 'shipping_country']
    fieldsets = [
        ('ORDER INFORMATION', { 'fields': ['id', 'token', 'total', 'created'] }),
        ('BILLING INFORMATION', { 'fields': ['billing_name', 'billing_address', 'billing_city', 'billing_postcode', 'billing_country', 'email'] }),
        ('SHIPPING INFORMATION', { 'fields': ['shipping_name', 'shipping_address', 'shipping_city', 'shipping_postcode', 'shipping_country'] }),
    ]

    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
