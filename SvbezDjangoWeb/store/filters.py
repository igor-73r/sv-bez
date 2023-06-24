import re
from .models import Products


def parse_query_string(query_string):
    pattern = r'(\w+)=([^&]+)'
    matches = re.findall(pattern, query_string)
    result = {}
    for match in matches:
        if match[0] in result:
            result[match[0]] += (match[1],)
        else:
            result[match[0]] = (match[1],)
    print(result)
    return result


def filtered_products(query_string):
    filter_parameters = parse_query_string(query_string)
    products = Products.objects.all()
    if 'brand' in filter_parameters:
        products = products.filter(brand__in=filter_parameters['brand'])
    if 'sale' in filter_parameters:
        products = products.filter(sale__isnull=False)
    if 'category' in filter_parameters:
        products = products.filter(category_id__in=filter_parameters['category'])
    return products

