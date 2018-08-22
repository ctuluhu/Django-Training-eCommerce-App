from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.get_products, name='products_all'),
    path('<slug:category_slug>/', views.get_products, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
]
