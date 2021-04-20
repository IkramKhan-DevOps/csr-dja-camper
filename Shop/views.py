import urllib

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

from Horsedch.models import Member


def add_product(request):
    return render(request, template_name="shop/products/add-product.html")


@login_required()
def all_products(request):
    social_account = SocialAccount.objects.get(user=request.user)
    context = {
        'social_account': social_account
    }
    return render(request, template_name="shop/products/all-products.html", context=context)


def my_products(request):
    return render(request, template_name="shop/products/my-products.html")


def rate_rental_experience(request):
    return render(request, template_name="shop/reviews/rate-rental-experience.html")


def checkout(request):
    return render(request, template_name="shop/take_on_rent/checkout.html")


def single_product_details(request):
    return render(request, template_name="shop/take_on_rent/product_details.html")


def profile_reviews(request):
    return render(request, template_name="shop/reviews/reviews.html")
