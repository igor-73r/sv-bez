from django.shortcuts import render, HttpResponse
from .models import Products, ProductsPropertiesValues, ProductsCategories
from django.template.defaulttags import register
from .filters import filtered_products
from .forms import BaseFilterForm


@register.filter
def get_range(value):
    return range(value)

def home_page(request):
    return render(request, "home.html", locals())


def store_view(request):
    form = BaseFilterForm()
    categories = ProductsCategories.objects.all()
    products = Products.objects.all()
    return render(request, "store/store.html", locals())


def filtered_store_view(request, query):
    if query is not None:
        categories = ProductsCategories.objects.all()
        products = filtered_products(query)
        form = BaseFilterForm(products)
        return render(request, "store/store.html", locals())


def product_view(request, slug):
    product = Products.objects.get(slug=slug)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
