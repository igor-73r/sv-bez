import os
import uuid


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
        case 'store_productsextraphotos':
            folder = 'photos/products/extra/'
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)
