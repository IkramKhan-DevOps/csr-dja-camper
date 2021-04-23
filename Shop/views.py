import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

from Horsedch.bll import has_social_account, get_member
from Horsedch.models import Member, Landlord
from Shop.forms import ProductForm
from Shop.models import Category


@login_required()
def add_product(request):
    social_account = ""
    member = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)
    category = Category.objects.all()
    if social_account:
        print(social_account)
    else:
        print("NO social accunt")

    if request.method == "POST":
        if "add-product" in request.POST:
            form = ProductForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                landlord = Landlord.objects.get(member__user=request.user)
                product = form.save(commit=False)
                product.landlord = landlord
                product.save()
                messages.success(request, "Action Completed Successfully!")
            else:
                messages.error(request, form.errors)
                print(form.errors)

    context = {
        'categories': category,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/add-product.html", context=context)


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
