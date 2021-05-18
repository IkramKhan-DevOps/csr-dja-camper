from django.forms import ModelForm

from Shop.models import Product, OrderCheckOutDetails


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class OrderCheckOutDetailsForm(ModelForm):
    class Meta:
        model = OrderCheckOutDetails
        fields = '__all__'
