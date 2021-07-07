from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.backends import UserModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from post_office import mail

from Horsedch import settings
from Horsedch.bll import create_member
from Horsedch.models import Member, Landlord, Renter, ContactInformation, SocialLinks
from Landlord.models import LandlordBankAccount, Language, SocialMediaLinks
from Shop.models import Order

import urllib
import requests


def sign_up_with_email(request):
    if request.user.is_authenticated:
        return redirect('My Account')
    else:
        if request.method == "POST":
            if request.POST.get("password") != request.POST.get("confirm_password"):
                messages.error(request, "Error: Password and confirm password doesn't match!")
            else:
                try:
                    user = User.objects.get_or_create(
                        first_name=request.POST.get("first_name"),
                        last_name=request.POST.get("last_name"),
                        email=request.POST.get("email_address"),
                        username=request.POST.get("email_address"),
                        password=make_password(request.POST.get("password")),
                        is_active=False
                    )
                    if user:
                        user = User.objects.get(username=request.POST.get("email_address"))
                    try:
                        member = Member.objects.create(
                            first_name=request.POST.get("first_name"),
                            last_name=request.POST.get("last_name"),
                            email_address=request.POST.get("email_address"),
                            role="Renter",
                            user=User.objects.get(username=request.POST.get("email_address"))
                        )
                        Renter.objects.create(member=member)
                        Landlord.objects.create(member=member)
                    except:
                        print("Problem in creating member")

                    current_site = get_current_site(request)
                    mail.send(
                        [request.POST.get("email_address")],
                        'no-reply@example.com',
                        template='welcome_email',
                        context={
                            'first_name': request.POST.get("first_name"),
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user=user)
                        },
                        priority='now',
                    )

                    messages.success(request, "Thank you for signing up. An email has been sent to " + request.POST.get(
                        "email_address") + ". Please confirm it to continue.")
                except:
                    messages.error(request, "Error: User with the email already exist!")

    return render(request, template_name="authentication/signup_using_email.html")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        member = Member.objects.get(user=user)
        member.email_verified = True
        member.save()
        messages.success(request, "Thank you for email confirmation, You can login now!")
        return redirect('Login')
    else:

        return HttpResponse("Invalid email validation link!")


def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get("email_address")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if Member.objects.filter(user=user).exists():
                return redirect("My Account")
        else:
            messages.error(request, "Invalid email address/password!")
    return render(request, template_name="authentication/auth_login.html")


def auth_logout(request):
    logout(request)
    return redirect('Login')


# This has been deferred. choose_role will be removed in next update 1.23.1
def choose_role(request):
    try:
        member = Member.objects.get(user=request.user)
        if member:
            if member.role == "Landlord":
                return redirect('My Account')
            else:
                return redirect('All Products')
    except:
        print("No member exist")

    return render(request, template_name="shop/role/choose-role.html")


# This has been deferred. update_member_profile will be removed in next update 1.23.1
@login_required()
def update_member_role(request, role):
    verified_email = False
    picture = "no-image-icon.png"
    try:
        social_account = SocialAccount.objects.filter(user=request.user)
        if social_account.exists():
            for data in social_account:
                verified_email = data.extra_data["verified_email"]
                picture = data.extra_data["picture"]
            member = Member.objects.create(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email_address=request.user.email,
                email_verified=verified_email,
                profile_picture=picture,
                role=role,
                user=request.user
            )

            user = User.objects.get(username=request.user.username)
            user.username = request.user.email
            user.save()
        else:
            print("Im in else of social account update member role")
            member = Member.objects.create(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email_address=request.user.email,
                role=role,
                user=request.user
            )
        try:
            if role == "Landlord":
                Landlord.objects.create(member=member)
            elif role == "Renter":
                Renter.objects.create(member=member)
        except:
            print("Oops")

    except ObjectDoesNotExist:
        print("No social account exist")
        print("social_account")
    return redirect('Edit Profile')  # Defere


def edit_profile(request):
    bank_account = ""
    member = ""
    try:
        member = Member.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, "")
    try:
        social_account = SocialAccount.objects.get(user=request.user)
    except ObjectDoesNotExist:
        social_account = ""
    try:
        if member.role == "Landlord":
            bank_account = LandlordBankAccount.objects.get(landlord__member=member)
    except:
        bank_account = ""

    try:
        language = Language.objects.get(landlord__member=member)
    except:
        language = ""
    try:
        social_links = SocialMediaLinks.objects.get(landlord__member=member)
    except ObjectDoesNotExist:
        social_links = ""

    if request.method == "POST":
        if "basic-information" in request.POST:
            try:
                profile_picture = request.FILES['profile_pic']
            except MultiValueDictKeyError:
                profile_picture = ""

            member_update = Member.objects.get(email_address=request.user.email)
            member_update.first_name = request.POST.get("first_name")
            member_update.last_name = request.POST.get("last_name")
            member_update.phone_number = request.POST.get("phone_number")
            member_update.street_address = request.POST.get("street_address")
            member_update.house_number = request.POST.get("house_number")
            member_update.zip_code = request.POST.get("zip_code")
            member_update.city = request.POST.get("city_name")
            member_update.country = request.POST.get("country_name")
            member_update.profile_picture = profile_picture
            member_update.save()
            messages.success(request, "Basic information updated successfully!")
            return redirect('Edit Profile')

        elif "bank-information" in request.POST:
            landlord = Landlord.objects.get(member=member)
            try:
                bank = LandlordBankAccount.objects.get(landlord=landlord)

                bank.first_name = request.POST.get("first_name")
                bank.last_name = request.POST.get("last_name")
                bank.email_address = request.POST.get("email_address")
                bank.phone_number = request.POST.get("phone_number")
                bank.street_address = request.POST.get("street_address")
                bank.house_number = request.POST.get("house_number")
                bank.zip_code = request.POST.get("zip_code")
                bank.city = request.POST.get("city_name")
                bank.country = request.POST.get("bank_country_name")
                bank.IBAN = request.POST.get("IBAN")
                bank.BIC = request.POST.get("BIC")
                bank.landlord = landlord
                bank.save()

            except LandlordBankAccount.DoesNotExist:
                LandlordBankAccount.objects.create(
                    first_name=request.POST.get("first_name"),
                    last_name=request.POST.get("last_name"),
                    email_address=request.POST.get("phone_number"),
                    phone_number=request.POST.get("email_address"),
                    street_address=request.POST.get("street_address"),
                    house_number=request.POST.get("house_number"),
                    zip_code=request.POST.get("zip_code"),
                    city=request.POST.get("city_name"),
                    country=request.POST.get("bank_country_name"),
                    IBAN=request.POST.get("IBAN"),
                    BIC=request.POST.get("BIC"),
                    landlord=landlord,
                )
            messages.success(request, "Bank account information updated successfully!")
            return redirect('Edit Profile')

        elif "additional-information" in request.POST:
            landlord = Landlord.objects.get(member=member)
            dutch = False
            french = False
            italian = False
            english = False
            if request.POST.get("dutch") == "on":
                dutch = True
            if request.POST.get("french") == "on":
                french = True
            if request.POST.get("italian") == "on":
                italian = True
            if request.POST.get("english") == "on":
                english = True

            try:
                language = Language.objects.get(landlord=landlord)
                language.dutch = dutch
                language.french = french
                language.italian = italian
                language.english = english
                language.save()
            except Language.DoesNotExist:
                Language.objects.create(
                    dutch=dutch,
                    french=french,
                    italian=italian,
                    english=english,
                    landlord=landlord
                )

            try:
                sm_links = SocialMediaLinks.objects.get(landlord=landlord)
                sm_links.facebook = request.POST.get("facebook_url")
                sm_links.instagram = request.POST.get("instagram_url")
                sm_links.save()
            except SocialMediaLinks.DoesNotExist:
                SocialMediaLinks.objects.create(

                    facebook=request.POST.get("facebook_url"),
                    instagram=request.POST.get("instagram_url"),
                    landlord=landlord
                )

            messages.success(request, "Additional information updated successfully!")
            return redirect('Edit Profile')

        elif "account-settings" in request.POST:
            user = User.objects.get(username=request.user.username)
            user.set_password(request.POST.get("password"))
            user.save()
            messages.success(request, "Password updated successfully!")

        elif "disconnect-social-account" in request.POST:
            user = User.objects.get(username=request.user.username)
            user.set_password(request.POST.get("password"))
            user.save()
            SocialAccount.objects.get(user=request.user).delete()
            messages.success(request, "Account disconnected successfully! Please login with your email to continue.")
            return redirect("Logout")
    context = {
        "member": member,
        "social_account": social_account,
        "bank_account": bank_account,
        "language": language,
        "social_links": social_links,

    }
    return render(request, template_name="authentication/profile/edit-profile.html", context=context)


@login_required()
def my_account(request):
    member = ""
    social_account = ""
    company_contact = ContactInformation.objects.latest('building_name')
    social_links = SocialLinks.objects.latest('facebook')

    try:
        if Member.objects.filter(user=request.user).exists():
            pass
        else:
            create_member(user=request.user)
        try:
            member = Member.objects.get(user=request.user)
        except ObjectDoesNotExist:
            messages.error(request, "")
        try:
            social_account = SocialAccount.objects.get(user=request.user)
        except ObjectDoesNotExist:
            social_account = ""
    except:
        print("Error in my_account")

    completed_order = Order.objects.filter(landlord__member__user=request.user, is_completed=True).count()
    orders = Order.objects.filter(landlord__member__user=request.user, is_completed=False)
    orders_amount = Order.objects.filter(landlord__member__user=request.user, is_completed=True)
    renter_orders = ""
    try:
        renter_orders = Order.objects.get(renter__member__user=request.user, is_completed=False)
    except:
        print("renter_orders does not exist")
    total_revenue = 0.0
    for order in orders_amount:
        total_revenue += order.landlord_amount

    context = {
        "member": member,
        "social_account": social_account,
        "completed_order": completed_order,
        "pending_order": orders.count(),
        "orders": orders,
        "total_revenue": total_revenue,
        "renter_orders": renter_orders,
        "company_contact": company_contact,
        "social_links": social_links,
    }
    return render(request, template_name="authentication/profile/my-account.html", context=context)


def switch_to_landlord(request):
    try:
        member = Member.objects.get(user=request.user)
        landlord = Landlord.objects.filter(member=member)
        if landlord.exists():
            print("landlord already exists")
            member.role = "Landlord"
            member.save()
        else:
            Landlord.objects.create(member=member)
            member.role = "Landlord"
            member.save()
    except:
        print("Error in switch_to_landlord")

    return redirect("My Account")


def switch_to_renter(request):
    try:
        member = Member.objects.get(user=request.user)
        member.role = "Renter"
        member.save()
    except:
        print("Error in switch_to_renter")

    return redirect("My Account")


class StripeAuthorizeView(View):

    def get(self, request):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('Login'))
        url = 'https://connect.stripe.com/oauth/authorize'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': f'http://localhost:8000/oauth/callback'
        }
        url = f'{url}?{urllib.parse.urlencode(params)}'
        return redirect(url)


class StripeAuthorizeCallbackView(View):
    login_required = True
    template_name = "authentication/login"

    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)
            print(resp.json())
            stripe_user_id = resp.json()['stripe_user_id']
            stripe_access_token = resp.json()['access_token']
            member = 13
            # if self.request.user.is_authenticated:
            #     member = Member.objects.get(user=self.request.user)
            # else:
            #     print("User is not authenticated")
            landlord = Landlord.objects.get(member_id=member)
            bank_info = LandlordBankAccount.objects.create(
                stripe_user_id=stripe_user_id,
                stripe_access_token=stripe_access_token,
                landlord=landlord
            )
        url = reverse('Edit Profile')
        response = redirect(url)
        return response
