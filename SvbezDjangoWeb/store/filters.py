from .models import Products, ProductsPropertiesValues


def filtered_products(props):
    products = Products.objects.all()
    price_range = [props.get('price_min'), props.get('price_max')]
    if price_range[0]:
        products = products.filter(price__gte=price_range[0])
    if price_range[1]:
        products = products.filter(price__lte=price_range[1])
    if 'brand' in props:
        products = products.filter(brand__in=props.getlist('brand'))
    return products


def extended_filter_products(props, category):
    products = Products.objects.filter(category_id=category)
    price_range = [props.get('price_min'), props.get('price_max')]
    if 'brand' in props:
        products = products.filter(brand__in=props.getlist('brand'))
    if price_range[0]:
        products = products.filter(price__gte=price_range[0])
    if price_range[1]:
        products = products.filter(price__lte=price_range[1])
    new_products = products
    print(new_products)
    if props:
        for i in products:
            property_value = ProductsPropertiesValues.objects.filter(product_id=i.id)
            for object in property_value:
                property_slug = object.property_name.property_name.slug
                if object.value not in props.getlist(property_slug) and property_slug in props:
                    new_products = new_products.exclude(pk=i.pk)
    return new_products
