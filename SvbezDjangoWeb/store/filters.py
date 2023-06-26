import re
from .models import Products, ProductsPropertiesValues, ProductsProperties


def filtered_products(props):
    products = Products.objects.all()
    for i in props:
        print(props.getlist(i))
        filter_str = i + '__in'
        products = products.filter(**{filter_str: props.getlist(i)})

    return products


def extended_filter_products(props, category):
    products = Products.objects.filter(category_id=category)
    new_products = products
    print(new_products)
    if props:
        for i in products:
            property_value = ProductsPropertiesValues.objects.filter(product_id=i.id)
            for object in property_value:
                property_slug = object.property_name.property_name.slug
                if object.value not in props.getlist(property_slug) and property_slug in props:
                    new_products = new_products.exclude(pk=i.pk)
                """print(object.property_name.property_name.slug, object.value)"""
    # print(products)
    return new_products
