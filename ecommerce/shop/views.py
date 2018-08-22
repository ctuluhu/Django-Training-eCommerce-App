from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .forms import SignUpForm
from .models import Category, Product


def home(request):
    return redirect('shop:products_all')


def get_products(request, category_slug=None):
    category_page = None
    products_list = None

    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products_list = Product.objects.filter(category=category_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)

    paginator = Paginator(products_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/category.html', { 'category' : category_page, 'products' : products })


def product_details(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    return render(request, 'shop/product.html', { 'product' : product })


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', { 'form' : form })


def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop:products_all')
            else:
                return redirect('signup_view')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/signin.html', { 'form' : form })


def signout_view(request):
    logout(request)
    return redirect('shop:products_all')
