from django.db import models
from django.contrib.admin import ModelAdmin
from django.urls import reverse


# Create your models here.

class ProductsProperties(models.Model):
    property_name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        verbose_name = 'Характеристики товаров'
        verbose_name_plural = 'Характеристики товаров'


class ProductsCategories(models.Model):
    category_name = models.CharField(primary_key=True, max_length=255)
    properties = models.ManyToManyField(ProductsProperties)

    class Meta:
        verbose_name = 'Категории товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.category_name


class Products(models.Model):
    brand = models.CharField("Бренд", max_length=255)
    model = models.CharField("Модель", max_length=255)
    price = models.IntegerField("Цена")
    description = models.TextField("Описание")
    category = models.ForeignKey(ProductsCategories,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name="Категория")
    image = models.ImageField(upload_to='photos/products/',
                              null=True, blank=True, max_length=255, verbose_name="Изображение")

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.model


    # def get_absolute_url(self):
    #     return reverse('product', kwargs={'product_id': self.pk})


class ProductsPropertiesValues(models.Model):
    class Meta:
        verbose_name = 'Значения характеристик'
        verbose_name_plural = 'Значения характеристик'
        unique_together = ['product_id', 'property_name']

    product_id = models.ForeignKey(Products,
                                   on_delete=models.CASCADE,
                                   verbose_name="ID Товара")

    property_name = models.ForeignKey(ProductsProperties,
                                      on_delete=models.CASCADE,
                                      verbose_name="Характеристика")

    value = models.CharField("Значение", max_length=255)
