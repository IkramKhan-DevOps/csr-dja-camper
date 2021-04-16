from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from Horsedch.models import Member


def choose_role(request):
    try:
        member = Member.objects.get(user=request.user).exists()
        if member:
            if member.role == "Landlord":
                return redirect('My Account')
            else:
                return redirect('All Products')
    except ObjectDoesNotExist:
        print("No member exist")

    return render(request, template_name="shop/role/choose-role.html")


@login_required()
def update_member_role(request, role):
    verified_email = False
    picture = "no-image-icon.png"
    try:
        social_account = SocialAccount.objects.get(user=request.user)
        if social_account is not None:
            verified_email = social_account.extra_data["verified_email"]
            picture = social_account.extra_data["picture"]
        member = Member.objects.get_or_create(
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email_address=request.user.email,
            email_verified=verified_email,
            profile_picture=picture,
            role=role,
            user=request.user
        )
    except ObjectDoesNotExist:
        print("No social account exist")
    return redirect('Edit Profile')


def edit_profile(request):
    return render(request, template_name="profile/edit-profile.html")


def my_account(request):
    return render(request, template_name="profile/my-account.html")