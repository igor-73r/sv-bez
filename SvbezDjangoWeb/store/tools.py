import uuid
import os
from django.core import mail


def encrypt(instance, filename):
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
            ['igorman.2016@gmail.com'],
            connection=connection,
        ).send()
