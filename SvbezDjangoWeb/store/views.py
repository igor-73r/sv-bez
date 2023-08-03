from django.shortcuts import render, redirect
from .models import Products, ProductsPropertiesValues, ProductsCategories, Brands, OurCustomers, ProductsExtraPhotos
from .filters import filtered_products
from .forms import CategoryFilterForm, FeedbackForm, ExtendedFeedbackForm, FullTextSearch, SortForm
from .tools import send_email, price_field_validation, extended_form_handler, search_product


def home_page(request):
    partners = Brands.objects.all().filter(is_partner=True)
    customers = OurCustomers.objects.all()
    ext_feedback_form = ExtendedFeedbackForm()
    feedback_form = FeedbackForm()
    if request.method == 'POST':
        if 'content' not in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                send_email(subject='Простое обращение',
                           body=f"Имя: {feedback_form.cleaned_data['username']}\n"
                                f"Тел: {feedback_form.cleaned_data['phone_number']}\n"
                                f"Почта: {feedback_form.cleaned_data['email']}\n")
                feedback_form = FeedbackForm()
        else:
            ext_feedback_form = extended_form_handler(request)
    return render(request, "home.html", locals())


def base_store_view(request, category=None):
    search_form = FullTextSearch()
    categories = ProductsCategories.objects.all()
    sort_form = SortForm(request.GET)
    try:
        selected = dict(sort_form.sort_types)[request.GET.get('sort_type')]
    except KeyError:
        selected = "По релевантности"
    ext_feedback_form = extended_form_handler(request, subject="Запрос на приобретение товара")
    props = request.GET
    if 'dismiss' in props:
        if category:
            return redirect("cat_store", category=category)
        else:
            return redirect("base_store")
    if request.GET.get('price_min') or request.GET.get('price_max'):
        props = price_field_validation(request)
    if category:
        products = filtered_products(props, category=category)
        form = CategoryFilterForm(props, category=category)
    else:
        products = filtered_products(props)
        form = CategoryFilterForm(props)
    if request.GET.get('search_field'):
        products = search_product(request.GET.get('search_field'))
        search_form = FullTextSearch(request.GET)
    if request.GET.get('sort_type'):
        match request.GET.get('sort_type'):
            case "price_descending":
                products = products.order_by("-price")
            case "price_ascending":
                products = products.order_by("price")

    return render(request, "store/store.html", locals())


def product_view(request, slug):
    ext_feedback_form = extended_form_handler(request, subject="Запрос на приобретение товара")
    product = Products.objects.get(slug=slug)
    extra_images = ProductsExtraPhotos.objects.filter(product_id=product.id)
    properties = ProductsPropertiesValues.objects.filter(product_id=product.id).order_by('property_name')
    return render(request, "store/product_detail.html", locals())
