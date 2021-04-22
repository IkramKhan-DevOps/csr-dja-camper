from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.utils.datastructures import MultiValueDictKeyError

from Horsedch.models import Member, Landlord, Renter
from Landlord.models import LandlordBankAccount, Language, SocialMediaLinks


def sign_up_with_email(request):
    if request.user.is_authenticated:
        return render(request.GET.get('next'))
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
                        is_active=True
                    )
                    user = authenticate(request, username=request.POST.get("email_address"),
                                        password=request.POST.get("password"))
                    if user is not None:
                        login(request, user)
                        return redirect('choose_role')
                except IntegrityError:
                    messages.error(request, "Error: User with the email already exist!")

    return render(request, template_name="authentication/signup_using_email.html")


def auth_login(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        if next_url != "":
            return redirect(next_url)
        print(next_url)
    return render(request, template_name="authentication/auth_login.html")


def auth_logout(request):
    logout(request)
    return redirect('Login')


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


@login_required()
def update_member_role(request, role):
    verified_email = False
    picture = "no-image-icon.png"
    try:
        social_account = SocialAccount.objects.filter(user=request.user)
        if social_account.exists():
            verified_email = social_account.extra_data["verified_email"]
            picture = social_account.extra_data["picture"]
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
    return redirect('Edit Profile')


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
            messages.success(request, "Account disconnect successfully! Please login with your email to continue.")
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
    return render(request, template_name="authentication/profile/my-account.html")
