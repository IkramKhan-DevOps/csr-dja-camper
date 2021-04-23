from allauth.socialaccount.models import SocialAccount

from Horsedch.models import Member


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