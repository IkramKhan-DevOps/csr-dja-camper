from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

from Horsedch.models import Landlord


class Category(models.Model):
    category_name = models.CharField(max_length=100, help_text="Enter category name here.")


class Product(models.Model):
    product_title = models.CharField(max_length=300)
    product_slug = AutoSlugField(populate_from="product_title")
    zip_code = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    price = models.FloatField()
    rental_type = models.CharField(max_length=15)
    brand = models.CharField(max_length=50)
    available_from = models.DateField()
    hide_item = models.BooleanField(default=False)
    product_description = models.TextField(max_length=500)
    offer_shipping = models.BooleanField(default=False)
    pick_up = models.BooleanField(default=True)
    image_1 = models.ImageField(upload_to="images/products/", default="no-image-icon.png")
    image_2 = models.ImageField(upload_to="images/products/", default="no-image-icon.png", null=True, blank=True)
    image_3 = models.ImageField(upload_to="images/products/", default="no-image-icon.png", null=True, blank=True)
    image_4 = models.ImageField(upload_to="images/products/", default="no-image-icon.png", null=True, blank=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.product_slug)


class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductMetaData(models.Model):
    meta_title = models.CharField(max_length=100)
    meta_keywords = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=300)
