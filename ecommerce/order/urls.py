from django.urls import path

from . import views


app_name = 'order'

urlpatterns = [
    path('thanks/<int:order_id>/', views.thanks_page, name='thanks_page'),
    path('history/', views.orders_history, name='orders_history'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
]
