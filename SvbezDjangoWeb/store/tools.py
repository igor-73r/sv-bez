import uuid
import os
from django.core import mail
from .config import EMAIL_USER


def encrypt(instance, filename):
    """
    UUID encryption of media file names in
    order to avoid duplication of names
    """
    folder = ''
    match instance._meta.db_table:
        case 'store_brands':
            folder = 'photos/brands-logos/'
        case 'store_products':
            folder = 'photos/products/'
        case 'store_ourcustomers':
            folder = 'photos/customers_companies/'
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)


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
