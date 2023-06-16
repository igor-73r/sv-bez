from django.contrib import admin
from django.urls import resolve
from .models import *


@admin.register(ProductsCategories)
class ProductsCategoriesAdmin(admin.ModelAdmin):
    filter_horizontal = ('properties',)


class ProductsPropertiesValuesAdmin(admin.TabularInline):  # DynamicModelAdminMixin
    model = ProductsPropertiesValues

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved:
            return self.parent_model.objects.get(pk=resolved.kwargs.get('object_id'))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        products_pk = self.get_parent_object_from_request(request).pk
        if db_field.name == "property_name":
            product_category = Products.objects.get(pk=products_pk).category
            kwargs["queryset"] = product_category.properties.all()
            print(kwargs['queryset'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'category')
    inlines = [ProductsPropertiesValuesAdmin]

    def get_inline_instances(self, request, obj=None):
        print(request, obj)
        for i in self.inlines:
            print(i)
        if not obj:
            return []
        else:
            return [inline(self.model, self.admin_site) for inline in self.inlines]


@admin.register(ProductsProperties)
class ProductsPropertiesAdmin(admin.ModelAdmin):
    search_fields = ['property_name']
