from django.shortcuts import render
from .models import Products, ProductsPropertiesValues, ProductsCategories
from .filters import filtered_products
from .forms import BaseFilterForm, CategoryFilterForm


def home_page(request):
    return render(request, "home.html", locals())


def store_view(request, query=None):
    form = BaseFilterForm()
    categories = ProductsCategories.objects.all()
    products = Products.objects.all()
    if query is not None:
        products = filtered_products(query)
        form = CategoryFilterForm(products)
    return render(request, "store/store.html", locals())


def product_view(request, slug):
    product = Products.objects.get(slug=slug)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
