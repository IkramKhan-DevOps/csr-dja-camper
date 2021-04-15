from datetime import datetime
from urllib.parse import urlencode

from django.conf.global_settings import AUTHENTICATION_BACKENDS
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from pip._vendor import requests
from allauth.socialaccount.models import SocialAccount
from Horsedch import settings
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
    how_it_works = HowItWork.objects.all()
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = ContactInformation.objects.latest('building_name')
    user_data = SocialAccount.objects.get(user=request.user)

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
        'user_data': user_data.extra_data

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
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = ContactInformation.objects.latest('building_name')
    try:
        condition = Condition.objects.latest('id')
    except:
        condition = None
    context = {
        'conditions': condition,
        'social_links': social_links,
        'company_contact': company_contact,
    }
    return render(request, template_name="site_pages/conditions.html", context=context)


def data_policy(request):
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = ContactInformation.objects.latest('building_name')
    try:
        policy = DataPolicy.objects.latest('id')
    except:
        policy = None
    context = {
        'data_policy': policy,
        'social_links': social_links,
        'company_contact': company_contact,
    }
    return render(request, template_name="site_pages/data-policy.html", context=context)


def fairplay(request):
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = ContactInformation.objects.latest('building_name')
    try:
        fair_play = FairPlay.objects.latest('id')
    except:
        fair_play = None
    context = {
        'fair_play': fair_play,
        'social_links': social_links,
        'company_contact': company_contact,
    }
    return render(request, template_name="site_pages/fairplay.html", context=context)


def imprint(request):
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = None
    try:
        company_contact = ContactInformation.objects.latest('id')
        imprint_data = Imprint.objects.latest('id')
    except:
        imprint_data = None
        if company_contact is None:
            company_contact = None
    context = {
        'imprint': imprint_data,
        'company_contact': company_contact,
        'social_links': social_links,
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


def login_via_google(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('login_via_google')
    )
    if 'code' in request.GET:
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        print(user_data)
        if email:
            user, _ = User.objects.get_or_create(email=email, username=email)
            gender = user_data.get('gender', '').lower()
            if gender == 'male':
                gender = 'M'
            elif gender == 'female':
                gender = 'F'
            else:
                gender = 'O'
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name'),
                'google_avatar': user_data.get('picture'),
                'gender': gender,
                'is_active': True
            }
            user.__dict__.update(data)
            user.save()
            user.backend = AUTHENTICATION_BACKENDS[0]
            login(request)

        else:
            messages.error(
                request,
                'Unable to login with google Please try again!'
            )
        return redirect('/')
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)


def login_via_facebook(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('login_via_facebook')
    )
    if 'code' in request.GET:
        code = request.GET.get('code')
        url = 'https://graph.facebook.com/v2.10/oauth/access_token'
        params = {
            'client_id': settings.FB_APP_ID,
            'client_secret': settings.FB_APP_SECRET,
            'code': code,
            'redirect_uri': redirect_uri,
        }
        response = requests.get(url, params=params)
        params = response.json()
        print("params before update: ", params)
        params.update({
            'fields': 'id,last_name,first_name,picture,birthday,email,gender'
        })
        print("params after update: ", params)
        url = 'https://graph.facebook.com/me'
        user_data = requests.get(url, params=params).json()
        print("user data printing: ", user_data)
        email = user_data.get('email')
        if email:
            user, _ = User.objects.get_or_create(email=email, username=email)
            gender = user_data.get('gender', '').lower()
            dob = user_data.get('birthday')
            if gender == 'male':
                gender = 'M'
            elif gender == 'female':
                gender = 'F'
            else:
                gender = 'O'
            data = {
                'first_name': user_data.get('first_name'),
                'last_name': user_data.get('last_name'),
                'fb_avatar': user_data.get('picture', {}).get('data', {}).get('url'),
                'gender': gender,
                'dob': datetime.strptime(dob, "%m/%d/%Y") if dob else None,
                'is_active': True
            }
            user.__dict__.update(data)
            user.save()
            user.backend = AUTHENTICATION_BACKENDS[0]
            login(request)
        else:
            messages.error(
                request,
                'Unable to login with Facebook Please try again!'
            )
        return redirect('/')
    else:
        url = "https://graph.facebook.com/oauth/authorize"
        params = {
            'client_id': settings.FB_APP_ID,
            'redirect_uri': redirect_uri,
            'scope': 'email,public_profile,user_birthday'
        }
        url += '?' + urlencode(params)
        return redirect(url)


def auth_logout(request):
    logout(request)
    return redirect('Login')