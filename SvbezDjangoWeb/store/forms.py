from django import forms
from .models import ProductsCategoriesProperties, ProductsPropertiesValues, Products


class CategoryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        products = None
        if kwargs.get('products'):
            products = kwargs.pop('products')
        super(CategoryFilterForm, self).__init__(*args)
        if products is not None:
            brands_list = Products.objects.values_list('brand', flat=True).distinct()
            brands = ()
            for i in brands_list:
                brands += (i, i),
            self.fields['brand'] = forms.MultipleChoiceField(choices=brands, label='Brand', required=False,
                                                             widget=forms.CheckboxSelectMultiple)
            if kwargs.get('category'):
                category = kwargs.pop('category')
                properties = ProductsCategoriesProperties.objects.filter(category_name=category)
                products_ids = Products.objects.values_list('id', flat=True)
                for i in properties:
                    queryset = ProductsPropertiesValues.objects.\
                        filter(product_id__in=products_ids, property_name=i).values_list('value', flat=True).distinct()
                    values = ()
                    for j in queryset:
                        values += (j, j),
                    self.fields[i.property_name.slug] = forms.MultipleChoiceField(choices=values, label=str(i), required=False,
                                                                    widget=forms.CheckboxSelectMultiple)
