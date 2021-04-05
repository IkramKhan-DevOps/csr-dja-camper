from django.contrib import messages
from django.shortcuts import render, redirect

from Horsedch.models import HowItWork, WhyHorsedCh, ContactInformation, Condition, DataPolicy, FairPlay, Imprint, \
    HeroSection, Box, AboutUs, GeneralFAQs, HowToRentFAQs, HowToListFAQs, SocialLinks, Team


def index_view(request):
    hero_section = HeroSection.objects.latest('site_title')
    box = Box.objects.all()
    about_us = AboutUs.objects.latest('heading')
    team = Team.objects.all()
    general_faqs = GeneralFAQs.objects.all()
    how_to_rent_faqs = HowToRentFAQs.objects.all()
    how_to_list_faqs = HowToListFAQs.objects.all()
    social_links = SocialLinks.objects.latest('facebook')
    how_it_works = HowItWork.objects.all()
    company_contact = ContactInformation.objects.latest('building_name')
    context = {
        'how_it_works': how_it_works,
        'company_contact': company_contact,
        'hero_section': hero_section,
        'boxes': box,
        'about_us': about_us,
        'team': team,
        'general_faqs': general_faqs,
        'how_to_rent_faqs': how_to_rent_faqs,
        'how_to_list_faqs': how_to_list_faqs,
        'social_links': social_links,

    }
    return render(request, template_name="site_pages/index.html", context=context)


def sign_up_view(request):
    return render(request, template_name="authentication/signup_using_email.html")


def add_product(request):
    return render(request, template_name="products/add-product.html")


def all_products(request):
    return render(request, template_name="products/all-products.html")


def my_products(request):
    return render(request, template_name="products/my-products.html")


def edit_profile(request):
    return render(request, template_name="profile/edit-profile.html")


def my_account(request):
    return render(request, template_name="profile/my-account.html")


def rate_rental_experience(request):
    return render(request, template_name="reviews/rate-rental-experience.html")


def profile_reviews(request):
    return render(request, template_name="reviews/reviews.html")


def conditions(request):
    try:
        condition = Condition.objects.latest('id')
    except:
        condition = None
    context = {
        'conditions': condition
    }
    return render(request, template_name="site_pages/conditions.html", context=context)


def data_policy(request):
    try:
        policy = DataPolicy.objects.latest('id')
    except:
        policy = None
    context = {
        'data_policy': policy
    }
    return render(request, template_name="site_pages/data-policy.html", context=context)


def fairplay(request):
    try:
        fair_play = FairPlay.objects.latest('id')
    except:
        fair_play = None
    context = {
        'fair_play': fair_play
    }
    return render(request, template_name="site_pages/fairplay.html", context=context)


def imprint(request):
    contact_information = None
    try:
        contact_information = ContactInformation.objects.latest('id')
        imprint_data = Imprint.objects.latest('id')
    except:
        imprint_data = None
        if contact_information is None:
            contact_information = None
    context = {
        'imprint': imprint_data,
        'contact_information': contact_information,
    }
    return render(request, template_name="site_pages/imprint.html", context=context)


def checkout(request):
    return render(request, template_name="take_on_rent/checkout.html")


def single_product_details(request):
    return render(request, template_name="take_on_rent/product_details.html")


def test(request):
    return render(request, template_name="site_pages/index.html")


def login(request):
    if request.method == "POST":
        if request.POST.get("email_address") == "seller@horsedch.com":
            return redirect('/my/account')
        elif request.POST.get("email_address") == "buyer@horsedch.com":
            return redirect('/my/account')
        else:
            messages.error(request, "Oops! Invalid username or password")

    return render(request, template_name="authentication/auth_login.html")
