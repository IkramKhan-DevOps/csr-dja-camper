from django.contrib import admin

from Horsedch.models import HowItWork, WhyHorsedCh, SocialLinks, ContactInformation, Condition, DataPolicy, FairPlay, \
    Imprint, HeroSection, Box, AboutUs, Team, GeneralFAQs, HowToRentFAQs, HowToListFAQs

admin.site.site_header = "Horsedch Administration Panel"
admin.site.index_title = "Horsedch Administration"

admin.site.register(HeroSection)
admin.site.register(Box)
admin.site.register(AboutUs)
admin.site.register(Team)
admin.site.register(GeneralFAQs)
admin.site.register(HowToRentFAQs)
admin.site.register(HowToListFAQs)
admin.site.register(HowItWork)
# admin.site.register(WhyHorsedCh)
admin.site.register(SocialLinks)
admin.site.register(ContactInformation)
admin.site.register(Condition)
admin.site.register(DataPolicy)
admin.site.register(FairPlay)
admin.site.register(Imprint)
