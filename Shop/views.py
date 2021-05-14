import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

from Horsedch.bll import has_social_account, get_member
from Horsedch.models import Member, Landlord
from Shop.forms import ProductForm
from Shop.models import Category, Product, Order


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
        print("NO social account")

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

    context = {
        'categories': category,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/add-product.html", context=context)


@login_required()
def all_products(request):
    social_account = ""
    member = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)
    context = {
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/all-products.html", context=context)


def my_products(request):
    social_account = ""
    member = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)

    products = ""
    try:
        landlord = Landlord.objects.get(member__user=request.user)
        # query = "SELECT Shop_product.id, product_title, price, rental_type, image_1, avg(stars_by_renter) AS stars FROM Shop_product left outer join Shop_order on Shop_product.id=Shop_order.product_id WHERE Shop_product.landlord_id=%s" % landlord.id
        products = Product.objects.filter(landlord=landlord)


    except:
        messages.error(request, "You don't have added any product yet.")

    context = {
        "products": products,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/my-products.html", context=context)


def edit_product(request, p_id):
    social_account = ""
    member = ""
    categories = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)
    product = ""
    try:
        product = Product.objects.get(id=p_id, landlord__member__user=request.user)
        categories = Category.objects.all()
    except:
        print("No product exists")
        # return to 404

    if request.method == "POST":
        product.product_title = request.POST.get("product_title")
        product.zip_code = request.POST.get("zip_code")
        product.city_name = request.POST.get("city_name")
        product.price = request.POST.get("price")
        product.rental_type = request.POST["rental_type"]
        product.brand = request.POST.get("brand")
        product.available_from = request.POST.get("available_from")
        product.hide_item = request.POST["hide_item"]
        product.product_description = request.POST.get("product_description")
        product.offer_shipping = request.POST["offer_shipping"]
        product.pick_up = request.POST["pick_up"]
        product.image_1 = request.POST["image_1"]
        product.image_2 = request.POST["image_2"]
        product.image_3 = request.POST["image_3"]
        product.image_4 = request.POST["image_4"]

        if request.POST["category_1"] != "Select":
            category_1 = request.POST["category_1"]
            messages.success(request, "Action Completed Successfully!")
        else:
            messages.error(request, "Please select product category.")
        if request.POST["category_2"] != "Select":
            category_2 = request.POST["category_2"]
        if request.POST["category_3"] != "Select":
            category_3 = request.POST["category_3"]
        product.save()

    context = {
        "product": product,
        'social_account': social_account,
        'member': member,
        'categories': categories,
    }

    return render(request, template_name="shop/products/edit-product.html", context=context)



def rate_rental_experience(request):
    return render(request, template_name="shop/reviews/rate-rental-experience.html")


def checkout(request):
    return render(request, template_name="shop/take_on_rent/checkout.html")


def single_product_details(request):
    return render(request, template_name="shop/take_on_rent/product_details.html")


def profile_reviews(request):
    return render(request, template_name="shop/reviews/reviews.html")
