from django.shortcuts import render
from .models import Products, ProductsPropertiesValues, ProductsCategories
from .filters import filtered_products, extended_filter_products
from .forms import CategoryFilterForm


def home_page(request):
    return render(request, "home.html", locals())


def price_field_validation(request):
    props = request.GET.copy()
    min_price, max_price = props.get('price_min'), props.get('price_max')
    if max_price != '' and min_price != '' and int(max_price) < int(min_price):
        props['price_min'], props['price_max'] = props['price_max'], props['price_min']
    return props


def base_store_view(request):
    categories = ProductsCategories.objects.all()
    props = request.GET
    if request.GET.get('price_min') or request.GET.get('price_max'):
        props = price_field_validation(request)
    products = filtered_products(props)
    form = CategoryFilterForm(props)
    return render(request, "store/store.html", locals())


def store_cat_view(request, category):
    categories = ProductsCategories.objects.all()
    props = request.GET
    if request.GET.get('price_min') or request.GET.get('price_max'):
        props = price_field_validation(request)
    products = extended_filter_products(props, category)
    form = CategoryFilterForm(props, category=category)
    return render(request, "store/store.html", locals())


def product_view(request, slug):
    product = Products.objects.get(slug=slug)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
