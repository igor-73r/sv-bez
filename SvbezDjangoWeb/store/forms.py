from django import forms
from .models import Brands


class BaseFilterForm(forms.Form):
    brands = Brands.objects.all()
    brand = forms.ModelMultipleChoiceField(queryset=brands, label='Brand', widget=forms.CheckboxSelectMultiple)
    price = forms.IntegerField()

    def __init__(self, products=None):
        super().__init__()
        if products is not None:
            brands = products.values_list('brand', flat=True)
            self.fields['brand'] = forms.ModelMultipleChoiceField(queryset=brands, label='Brand',
                                                              widget=forms.CheckboxSelectMultiple)


class CategoryFilterForm(BaseFilterForm):
    your_name = forms.CharField(label='Your name', max_length=100)
