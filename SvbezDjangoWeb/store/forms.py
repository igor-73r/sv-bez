from django import forms
from .models import ProductsCategoriesProperties, ProductsPropertiesValues, Products
from django.db.models import Max, Min


class CategoryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args)
        self.label_suffix = ""
        custom_checkbox_widget = forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'})
        if 'category' in kwargs:
            products = Products.objects.filter(category=kwargs.get('category'))
            brands_list = products.values_list('brand', flat=True).distinct()
            available_price = products.aggregate(Min('price'), Max('price'))
        else:
            products = Products.objects.all()
            brands_list = products.values_list('brand', flat=True).distinct()
            available_price = products.aggregate(Min('price'), Max('price'))
        min_price = available_price['price__min']
        max_price = available_price['price__max']
        brands = ()
        for i in brands_list:
            brands += (i, i),
        self.fields['brand'] = forms.MultipleChoiceField(choices=brands, label='Бренд', required=False,
                                                         widget=forms.CheckboxSelectMultiple)
        self.fields['price_min'] = forms.IntegerField(required=False,
                                                      widget=forms.NumberInput(attrs={
                                                          'placeholder': 'От ' + str(min_price)}),
                                                      min_value=min_price, max_value=max_price)
        self.fields['price_max'] = forms.IntegerField(required=False,
                                                      widget=forms.NumberInput(attrs={
                                                          'placeholder': 'До ' + str(max_price)}),
                                                      min_value=min_price, max_value=max_price)

        if 'category' in kwargs:
            category = kwargs.pop('category')
            properties = ProductsCategoriesProperties.objects.filter(category_name=category)
            products_ids = Products.objects.values_list('id', flat=True)
            for i in properties:
                queryset = ProductsPropertiesValues.objects.\
                    filter(product_id__in=products_ids, property_name=i).values_list('value', flat=True).distinct()
                values = ()
                for j in queryset:
                    values += (j, j),
                self.fields[i.property_name.slug] = forms.MultipleChoiceField(choices=values, label=str(i),
                                                                              required=False,
                                                                              widget=forms.CheckboxSelectMultiple)
