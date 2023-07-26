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


class ProductsPropertiesValuesAdmin(admin.TabularInline):
    model = ProductsPropertiesValues
    extra = 0

    def get_parent_object_from_request(self, request):
        """
        Get object of parent table of inline block
        """
        resolved = resolve(request.path_info)
        if resolved:
            return self.parent_model.objects.get(pk=resolved.kwargs.get('object_id'))
        return None

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Creates a queryset with characteristics corresponding to the selected category
        """
        products_category = self.get_parent_object_from_request(request).category
        if db_field.name == "property_name":
            product_cp = ProductsCategoriesProperties.objects.filter(category_name=products_category)
            kwargs["queryset"] = product_cp.order_by('property_priority')
            self.extra = len(kwargs['queryset'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExtraPhotosAdmin(admin.TabularInline):
    model = ProductsExtraPhotos
    readonly_fields = ('id', 'image_tag',)
    extra = 1


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    search_fields = ('model',)
    list_display = ('brand', 'model', 'price', 'category', 'is_published', )
    prepopulated_fields = {"slug": ("brand", "model")}
    autocomplete_fields = ('brand', 'category')
    inlines = [ExtraPhotosAdmin, ProductsPropertiesValuesAdmin]

    def get_inline_instances(self, request, obj=None):
        """
        Handles an exception in which,
        if the products do not have a category,
        the inline block cannot be displayed
        """
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


admin.site.register(OurCustomers)
