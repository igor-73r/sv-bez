from django.db import models
from django.urls import reverse
from .db_handler import encrypt


class ProductsProperties(models.Model):
    property_name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товаров'

    def __str__(self):
        return self.property_name


class ProductsCategories(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    properties = models.ManyToManyField(ProductsProperties, through='ProductsCategoriesProperties')
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.category_name


class Brands(models.Model):
    brand = models.CharField(max_length=255, unique=True)
    brand_logo = models.ImageField(upload_to=encrypt,
                                   null=True, blank=True, max_length=255, verbose_name="Логотип")
    is_partner = models.BooleanField("Партнер", default=False)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.brand


class ProductsCategoriesProperties(models.Model):
    category_name = models.ForeignKey(ProductsCategories, on_delete=models.CASCADE)
    property_name = models.ForeignKey(ProductsProperties, on_delete=models.CASCADE)
    property_priority = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["property_priority"]
        unique_together = (('category_name', 'property_name'),)

    def __str__(self):
        return str(self.property_name)


class Products(models.Model):
    is_published = models.BooleanField("Опубликовать", default=True)
    brand = models.ForeignKey(Brands, to_field='brand', null=True,
                              on_delete=models.SET_NULL, verbose_name="Бренд")
    model = models.CharField("Модель", max_length=255)
    slug = models.SlugField('URL', max_length=255, unique=True, db_index=True)
    price = models.IntegerField("Цена")
    sale = models.IntegerField("Скидка", null=True, blank=True)
    description = models.TextField("Описание")
    category = models.ForeignKey(ProductsCategories,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name="Категория")
    image = models.ImageField(upload_to=encrypt,
                              null=True, blank=True, max_length=255, verbose_name="Изображение")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.slug})


class ProductsPropertiesValues(models.Model):
    product_id = models.ForeignKey(Products,
                                   on_delete=models.CASCADE,
                                   verbose_name="ID Товара")

    property_name = models.ForeignKey(ProductsCategoriesProperties,
                                      on_delete=models.CASCADE,
                                      verbose_name="Характеристика")

    value = models.CharField("Значение", max_length=255)

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'
        unique_together = ['product_id', 'property_name']

    def __str__(self):
        return self.value


class OurCustomers(models.Model):
    company_name = models.CharField("Название компании", max_length=255)
    company_logo = models.ImageField(upload_to=encrypt,
                                     null=True, blank=True, max_length=255, verbose_name="Логотип компании")
    company_description = models.TextField("Описание")

    class Meta:
        verbose_name = 'Наш клиент'
        verbose_name_plural = 'Наши клиенты'

    def __str__(self):
        return self.company_name
