from django.shortcuts import render, HttpResponse
from .models import Products
from django.template.defaulttags import register


@register.filter
def get_range(value):
    return range(value)


def store_view(request):
    products = Products.objects.all()
    return render(request, "store/store.html", locals())
