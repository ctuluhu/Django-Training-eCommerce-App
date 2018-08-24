from django.db.models import Q
from django.shortcuts import render

from shop.models import Product


def search(request):
    query = None
    products = None
    if 'search' in request.GET:
        query = request.GET.get('search')
        products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))

    return render(request, 'search.html', { 'query': query, 'products': products })
