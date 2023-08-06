from django.core import mail
from django.contrib.postgres.search import SearchVector
from .config import EMAIL_USER
from .forms import ExtendedFeedbackForm
from .models import Products


def clear_my_cookie(request, response):
    for cookie in request.COOKIES:
        if request.COOKIES[cookie] == "hint":
            response.delete_cookie(cookie)
    return response


def search_product(product=None):
    searched_products = Products.objects.annotate(search=SearchVector('brand') +
                                                         SearchVector('model') +
                                                         SearchVector('description')).filter(search=product)
    return searched_products


def extended_form_handler(request, subject="Расширенное обращение"):
    extended_form = ExtendedFeedbackForm()
    if request.method == 'POST':
        extended_form = ExtendedFeedbackForm(request.POST)
        if extended_form.is_valid():
            send_email(subject=subject,
                       body=f"Имя: {extended_form.cleaned_data['username']}\n"
                            f"Тел: {extended_form.cleaned_data['phone_number']}\n"
                            f"Почта: {extended_form.cleaned_data['email']}\n"
                            f"--- --- ---\n"
                            f"Сообщение: {extended_form.cleaned_data['content']}")
            extended_form = ExtendedFeedbackForm()
    return extended_form


def send_email(subject, body):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject,
            body,
            "*",
            [EMAIL_USER],
            connection=connection,
        ).send()


def price_field_validation(request):
    props = request.GET.copy()
    min_price, max_price = props.get('price_min'), props.get('price_max')
    if max_price != '' and min_price != '' and int(max_price) < int(min_price):
        props['price_min'], props['price_max'] = props['price_max'], props['price_min']
    return props
