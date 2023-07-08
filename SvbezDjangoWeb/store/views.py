from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Products, ProductsPropertiesValues, ProductsCategories, Brands, OurCustomers
from .filters import filtered_products, extended_filter_products
from .forms import CategoryFilterForm, FeedbackForm
from django.core import mail


def home_page(request):
    partners = Brands.objects.all().filter(is_partner=True)
    customers = OurCustomers.objects.all()
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            send_email('Простое обращение',
                       f"Имя: {feedback_form.cleaned_data['username']}\n"
                       f"Тел: {feedback_form.cleaned_data['phone_number']}\n"
                       f"Почта: {feedback_form.cleaned_data['email']}\n",
                       feedback_form.cleaned_data['email'])
    else:
        feedback_form = FeedbackForm()
    return render(request, "home.html", locals())


def send_email(subject, body, from_email):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject,
            body,
            from_email,
            ['igorman.2016@gmail.com'],
            connection=connection,
        ).send()


def price_field_validation(request):
    props = request.GET.copy()
    min_price, max_price = props.get('price_min'), props.get('price_max')
    if max_price != '' and min_price != '' and int(max_price) < int(min_price):
        props['price_min'], props['price_max'] = props['price_max'], props['price_min']
    return props


def base_store_view(request):
    categories = ProductsCategories.objects.all()
    props = request.GET
    if 'dismiss' in props:
        return redirect('base_store')
    if request.GET.get('price_min') or request.GET.get('price_max'):
        props = price_field_validation(request)
    products = filtered_products(props)
    form = CategoryFilterForm(props)
    return render(request, "store/store.html", locals())


def store_cat_view(request, category):
    categories = ProductsCategories.objects.all()
    props = request.GET
    if 'dismiss' in props:
        return redirect('cat_store', category)
    if request.GET.get('price_min') or request.GET.get('price_max'):
        props = price_field_validation(request)
    products = extended_filter_products(props, category)
    form = CategoryFilterForm(props, category=category)
    return render(request, "store/store.html", locals())


def product_view(request, slug):
    product = Products.objects.get(slug=slug)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
