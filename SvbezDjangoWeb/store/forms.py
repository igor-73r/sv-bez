from django import forms
from .models import Brands, ProductsCategoriesProperties, ProductsPropertiesValues


class BaseFilterForm(forms.Form):
    brands = Brands.objects.all()
    brand = forms.ModelMultipleChoiceField(queryset=brands, label='Brand', widget=forms.CheckboxSelectMultiple)
    price = forms.IntegerField()


class CategoryFilterForm(BaseFilterForm):
    def __init__(self, products=None):
        super().__init__()
        if products is not None:
            brands = products.values_list('brand', flat=True)
            self.fields['brand'] = forms.ModelMultipleChoiceField(queryset=brands, label='Brand',
                                                              widget=forms.CheckboxSelectMultiple)
            category = products[0].category
            properties = ProductsCategoriesProperties.objects.filter(category_name=category)
            products_ids = products.values_list('id', flat=True)
            for i in properties:
                queryset = ProductsPropertiesValues.objects.\
                    filter(product_id__in=products_ids, property_name=i).values_list('value', flat=True).distinct()
                self.fields[str(i)] = forms.ModelMultipleChoiceField(queryset=queryset, label=str(i),
                                                              widget=forms.CheckboxSelectMultiple)
