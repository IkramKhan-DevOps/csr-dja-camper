from django.shortcuts import render

from Horsedch.models import HowItWork, ContactInformation, Condition, DataPolicy, FairPlay, Imprint, \
    HeroSection, Box, AboutUs, GeneralFAQs, HowToRentFAQs, HowToListFAQs, SocialLinks, Team, ObjectOwnerFAQs, Partner, \
    CustomerCare
from Shop.models import Product, Order


def index_view(request):
    hero_section = HeroSection.objects.latest('site_title')
    box = Box.objects.all()
    about_us = AboutUs.objects.latest('heading')
    team = CustomerCare.objects.all()
    general_faqs = GeneralFAQs.objects.all()
    how_to_rent_faqs = HowToRentFAQs.objects.all()
    how_to_list_faqs = HowToListFAQs.objects.all()
    how_it_works = HowItWork.objects.filter(is_active=True)
    social_links = SocialLinks.objects.latest('facebook')
    company_contact = ContactInformation.objects.latest('building_name')
    recent_products = Product.objects.all()[:4][::-1]
    query = "SELECT Shop_order.id, Shop_order.product_id,count('Shop_order.product_id') AS total_order From Shop_order GROUP BY Shop_order.product_id LIMIT 4"
    popular_products = Order.objects.raw(query)
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
        'recent_products': recent_products,
        'popular_products': popular_products,

    }
    return render(request, template_name="site_pages/index.html", context=context)


def about_us(request):
    who_we_are = AboutUs.objects.latest('heading')
    company_contact = ContactInformation.objects.latest('building_name')
    social_links = SocialLinks.objects.latest('facebook')
    team = Team.objects.all()
    context = {
        'company_contact': company_contact,
        'about_us': who_we_are,
        'team': team,
        'social_links': social_links,

    }
    return render(request, template_name="site_pages/about-us.html", context=context)


def faqs(request):
    general_faqs = GeneralFAQs.objects.all()
    how_to_rent_faqs = HowToRentFAQs.objects.all()
    how_to_list_faqs = HowToListFAQs.objects.all()
    company_contact = ContactInformation.objects.latest('building_name')
    social_links = SocialLinks.objects.latest('facebook')
    context = {
        'company_contact': company_contact,
        'social_links': social_links,
        'general_faqs': general_faqs,
        'how_to_rent_faqs': how_to_rent_faqs,
        'how_to_list_faqs': how_to_list_faqs,

    }
    return render(request, template_name="site_pages/faqs.html", context=context)


def faqs_object_owners(request):
    object_owner_faqs = ObjectOwnerFAQs.objects.all()
    company_contact = ContactInformation.objects.latest('building_name')
    social_links = SocialLinks.objects.latest('facebook')
    context = {
        'company_contact': company_contact,
        'social_links': social_links,
        'object_owner_faqs': object_owner_faqs,

    }
    return render(request, template_name="site_pages/faqs-object-owners.html", context=context)


def our_partners(request):
    partners = Partner.objects.filter(is_active=True)
    company_contact = ContactInformation.objects.latest('building_name')
    social_links = SocialLinks.objects.latest('facebook')
    context = {
        'company_contact': company_contact,
        'social_links': social_links,
        'partners': partners,

    }
    return render(request, template_name="site_pages/partners.html",context=context )


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


def test(request):
    return render(request, template_name="site_pages/index.html")


# def login_via_google(request):
#     redirect_uri = "%s://%s%s" % (
#         request.scheme, request.get_host(), reverse('login_via_google')
#     )
#     if 'code' in request.GET:
#         params = {
#             'grant_type': 'authorization_code',
#             'code': request.GET.get('code'),
#             'redirect_uri': redirect_uri,
#             'client_id': settings.GP_CLIENT_ID,
#             'client_secret': settings.GP_CLIENT_SECRET
#         }
#         url = 'https://accounts.google.com/o/oauth2/token'
#         response = requests.post(url, data=params)
#         url = 'https://www.googleapis.com/oauth2/v1/userinfo'
#         access_token = response.json().get('access_token')
#         response = requests.get(url, params={'access_token': access_token})
#         user_data = response.json()
#         email = user_data.get('email')
#         print(user_data)
#         if email:
#             user, _ = User.objects.get_or_create(email=email, username=email)
#             gender = user_data.get('gender', '').lower()
#             if gender == 'male':
#                 gender = 'M'
#             elif gender == 'female':
#                 gender = 'F'
#             else:
#                 gender = 'O'
#             data = {
#                 'first_name': user_data.get('name', '').split()[0],
#                 'last_name': user_data.get('family_name'),
#                 'google_avatar': user_data.get('picture'),
#                 'gender': gender,
#                 'is_active': True
#             }
#             user.__dict__.update(data)
#             user.save()
#             user.backend = AUTHENTICATION_BACKENDS[0]
#             login(request)
#
#         else:
#             messages.error(
#                 request,
#                 'Unable to login with google Please try again!'
#             )
#         return redirect('/')
#     else:
#         url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
#         scope = [
#             "https://www.googleapis.com/auth/userinfo.profile",
#             "https://www.googleapis.com/auth/userinfo.email"
#         ]
#         scope = " ".join(scope)
#         url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
#         return redirect(url)
#
#
# def login_via_facebook(request):
#     redirect_uri = "%s://%s%s" % (
#         request.scheme, request.get_host(), reverse('login_via_facebook')
#     )
#     if 'code' in request.GET:
#         code = request.GET.get('code')
#         url = 'https://graph.facebook.com/v2.10/oauth/access_token'
#         params = {
#             'client_id': settings.FB_APP_ID,
#             'client_secret': settings.FB_APP_SECRET,
#             'code': code,
#             'redirect_uri': redirect_uri,
#         }
#         response = requests.get(url, params=params)
#         params = response.json()
#         print("params before update: ", params)
#         params.update({
#             'fields': 'id,last_name,first_name,picture,birthday,email,gender'
#         })
#         print("params after update: ", params)
#         url = 'https://graph.facebook.com/me'
#         user_data = requests.get(url, params=params).json()
#         print("user data printing: ", user_data)
#         email = user_data.get('email')
#         if email:
#             user, _ = User.objects.get_or_create(email=email, username=email)
#             gender = user_data.get('gender', '').lower()
#             dob = user_data.get('birthday')
#             if gender == 'male':
#                 gender = 'M'
#             elif gender == 'female':
#                 gender = 'F'
#             else:
#                 gender = 'O'
#             data = {
#                 'first_name': user_data.get('first_name'),
#                 'last_name': user_data.get('last_name'),
#                 'fb_avatar': user_data.get('picture', {}).get('data', {}).get('url'),
#                 'gender': gender,
#                 'dob': datetime.strptime(dob, "%m/%d/%Y") if dob else None,
#                 'is_active': True
#             }
#             user.__dict__.update(data)
#             user.save()
#             user.backend = AUTHENTICATION_BACKENDS[0]
#             login(request)
#         else:
#             messages.error(
#                 request,
#                 'Unable to login with Facebook Please try again!'
#             )
#         return redirect('/')
#     else:
#         url = "https://graph.facebook.com/oauth/authorize"
#         params = {
#             'client_id': settings.FB_APP_ID,
#             'redirect_uri': redirect_uri,
#             'scope': 'email,public_profile,user_birthday'
#         }
#         url += '?' + urlencode(params)
#         return redirect(url)



