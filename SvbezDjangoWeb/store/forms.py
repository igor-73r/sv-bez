from django import forms
from .models import ProductsCategoriesProperties, ProductsPropertiesValues, Products
from django.db.models import Max, Min
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=50, label="Ваше имя", required=True)
    phone_number = forms.CharField(max_length=11, required=True, label="Номер телефона")
    email = forms.EmailField(required=False, label="Email")
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible, label='')


class ExtendedFeedbackForm(FeedbackForm):
    content = forms.CharField(widget=forms.Textarea, required=False, label="Сообщение", max_length=700)


class FullTextSearch(forms.Form):
    search_field = forms.CharField(max_length=255,
                                   widget=forms.TextInput(attrs={'placeholder': 'Найти'}),
                                   label="", required=False)


class SortForm(forms.Form):
    sort_types = (
        ("", "По релевантности"),
        ("price_descending", "Сначало дороже"),
        ("price_ascending", "Сначало дешевле"),
    )

    sort_type = forms.ChoiceField(choices=sort_types, required=False, label="", widget=forms.RadioSelect)


class CategoryFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CategoryFilterForm, self).__init__(*args)
        self.label_suffix = ""
        if 'category' in kwargs:
            products = Products.objects.filter(category=kwargs.get('category'))
            brands_list = products.values_list('brand', flat=True).distinct()
            available_price = products.aggregate(Min('price'), Max('price'))
        else:
            products = Products.objects.all()
            brands_list = products.values_list('brand', flat=True).distinct()
            available_price = products.filter(is_published=True).aggregate(Min('price'), Max('price'))
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
                                                      min_value=0)
        self.fields['price_max'] = forms.IntegerField(required=False,
                                                      widget=forms.NumberInput(attrs={
                                                          'placeholder': 'До ' + str(max_price)}),
                                                      min_value=0)

        if 'category' in kwargs:
            category = kwargs.pop('category')
            properties = ProductsCategoriesProperties.objects.filter(category_name=category)
            products_ids = Products.objects.values_list('id', flat=True)
            for i in properties:
                if i.property_name.filter_available:
                    queryset = ProductsPropertiesValues.objects.\
                        filter(product_id__in=products_ids, property_name=i).values_list('value', flat=True).distinct()
                    values = ()
                    for j in queryset:
                        values += (j, j),
                    self.fields[i.property_name.slug] = forms.MultipleChoiceField(choices=values, label=str(i),
                                                                                  required=False,
                                                                                  widget=forms.CheckboxSelectMultiple)
