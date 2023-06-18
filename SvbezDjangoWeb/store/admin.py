from django.contrib import admin
from django.urls import resolve
from .models import *


class ProductsCategoriesPropAdmin(admin.TabularInline):
    model = ProductsCategoriesProperties
    autocomplete_fields = ('property_name',)


@admin.register(ProductsCategories)
class ProductsCategoriesAdmin(admin.ModelAdmin):
    search_fields = ('category_name',)
    prepopulated_fields = {"slug": ("category_name",)}
    inlines = [ProductsCategoriesPropAdmin]


class ProductsPropertiesValuesAdmin(admin.TabularInline):  # DynamicModelAdminMixin
    model = ProductsPropertiesValues
    extra = 40

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved:
            return self.parent_model.objects.get(pk=resolved.kwargs.get('object_id'))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        products_category = self.get_parent_object_from_request(request).category
        if db_field.name == "property_name":
            product_cp = ProductsCategoriesProperties.objects.filter(category_name=products_category)
            kwargs["queryset"] = product_cp.order_by('property_priority')
            print(kwargs['queryset'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'category', 'is_published')
    prepopulated_fields = {"slug": ("brand", "model")}
    autocomplete_fields = ('brand', 'category')
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
    prepopulated_fields = {"slug": ("property_name",)}


@admin.register(Brands)
class BrandsAdmin(admin.ModelAdmin):
    search_fields = ('brand',)
