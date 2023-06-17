from django.shortcuts import render
from .models import * #Products, ProductsPropertiesValues, ProductsCategories
from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)

def home_page(request):
    return render(request, "home.html", locals())


def store_view(request):
    products = Products.objects.all()
    return render(request, "store/store.html", locals())


def product_view(request, pk):
    product = Products.objects.get(slug=pk)
    ordered_properties = product.category.properties.all().order_by('productscategoriesproperties')
    print(ordered_properties)

    properties = ProductsPropertiesValues.objects.filter(product_id=product.id,
                                                         property_name__in=ordered_properties)
    return render(request, "store/product_detail.html", locals())
