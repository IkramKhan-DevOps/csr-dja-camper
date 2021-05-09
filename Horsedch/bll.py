from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from Horsedch.models import Member, Renter


def has_social_account(user):
    social_account = SocialAccount.objects.get(user=user)
    if social_account:
        return social_account
    else:
        return False


def get_member(user):
    member = Member.objects.get(user=user)
    if member:
        return member
    else:
        return False


def check_member(user):
    member = Member.objects.get(user=user)
    if member:
        return True
    else:
        return False


def create_member(user):
    verified_email = False
    picture = "no-image-icon.png"
    try:
        social_account = SocialAccount.objects.filter(user=user)
        if social_account.exists():
            for data in social_account:
                verified_email = data.extra_data["verified_email"]
                picture = data.extra_data["picture"]

            member = Member.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email_address=user.email,
                email_verified=verified_email,
                profile_picture=picture,
                role="Renter",
                user=user
            )
            user = User.objects.get(username=user.username)
            user.username = user.email
            user.save()

            Renter.objects.create(member=member)

    except ObjectDoesNotExist:
        print("No social account exist")

