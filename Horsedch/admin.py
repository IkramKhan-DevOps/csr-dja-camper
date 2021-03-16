from django.contrib import admin

from Horsedch.models import HowItWork, WhyHorsedCh, SocialLinks, ContactInformation, Condition, DataPolicy, FairPlay, \
    Imprint

admin.site.site_header = "Horsedch Administration | Root Access"
admin.site.index_title = "Horsedch Administration"

admin.site.register(HowItWork)
admin.site.register(WhyHorsedCh)
admin.site.register(SocialLinks)
admin.site.register(ContactInformation)
admin.site.register(Condition)
admin.site.register(DataPolicy)
admin.site.register(FairPlay)
admin.site.register(Imprint)
