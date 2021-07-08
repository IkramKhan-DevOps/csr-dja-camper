from django.db import models
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

from Horsedch.models import Landlord, Renter


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
    category_1 = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_1")
    category_2 = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, verbose_name="Category 2", null=True, blank=True, related_name="category_2" )
    category_3 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category 3", null=True, blank=True, related_name="category_3")

    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, blank=True)

    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_on = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.product_slug)


# Deferred
# class ProductCategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductMetaData(models.Model):
    meta_title = models.CharField(max_length=100)
    meta_keywords = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=300)


class Order(models.Model):
    total_amount = models.FloatField()
    landlord_amount = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE)

    is_completed = models.BooleanField(default=False)

    stars_by_renter = models.FloatField(null=True, blank=True)
    stars_by_landlord = models.FloatField(null=True, blank=True)
    comment_by_renter = models.CharField(max_length=500, null=True, blank=True)
    comment_by_landlord = models.CharField(max_length=500, null=True, blank=True)


class OrderCheckOutDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=50)
    street_address = models.TextField(max_length=300)
    house_number = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    language = models.CharField(max_length=50)
    book_from = models.DateField()
    book_till = models.DateField()
    pick_up = models.BooleanField(default=False)
    delivery = models.BooleanField(default=True)

    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.email_address


