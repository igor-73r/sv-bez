from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponse, redirect
from .models import Products, ProductsPropertiesValues, ProductsCategories
from .filters import filtered_products, extended_filter_products
from .forms import CategoryFilterForm


def home_page(request):
    return render(request, "home.html", locals())


def generate_query(form):
    print(form.cleaned_data)
    query = ""
    for i in form.cleaned_data:
        if form.cleaned_data[i]:
            query += f"{i}="
            for j in form.cleaned_data[i]:
                query += f"&{j}"
            query += "&&"
    return query


def base_store_view(request):
    categories = ProductsCategories.objects.all()
    products = filtered_products(request.GET)
    form = CategoryFilterForm(request.GET, products=products)
    return render(request, "store/store.html", locals())


def store_cat_view(request, category):
    categories = ProductsCategories.objects.all()
    products = extended_filter_products(request.GET, category)
    form = CategoryFilterForm(request.GET, products=products, category=category)
    return render(request, "store/store.html", locals())


def product_view(request, slug):
    product = Products.objects.get(slug=slug)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
