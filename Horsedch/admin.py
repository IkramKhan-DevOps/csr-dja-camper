from django.contrib import admin

from Horsedch.models import HowItWork, WhyHorsedCh, SocialLinks, ContactInformation, Condition, DataPolicy, FairPlay, \
    Imprint, HeroSection, Box, AboutUs, Team, GeneralFAQs, HowToRentFAQs, HowToListFAQs, ObjectOwnerFAQs, Partner, \
    CustomerCare
from Shop.models import Product, Category

admin.site.site_header = "Horsed Administration Panel"
admin.site.index_title = "Horsed Administration"


class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['site_title', 'site_description', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not HeroSection.objects.exists()


class BoxAdmin(admin.ModelAdmin):
    list_display = ['box_title', 'box_description', 'is_active']


class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['heading', 'sub_heading', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not AboutUs.objects.exists()


class TeamAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation', 'facebook_link', 'instagram_link', 'email_address', 'person_img']


class GeneralFAQsAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class HowToRentFAQsAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class HowToListFAQsAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class ObjectOwnerFAQsAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'partner_logo']


class HowItWorkAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'picture']


class WhyHorsedChAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'picture']


class SocialLinksAdmin(admin.ModelAdmin):
    list_display = ['facebook', 'instagram', 'linkedIn', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not SocialLinks.objects.exists()


class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['building_name', 'street', 'post_code', 'email_address', 'phone_number']

    def has_add_permission(self, *args, **kwargs):
        return not ContactInformation.objects.exists()


class ConditionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not Condition.objects.exists()


class DataPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not DataPolicy.objects.exists()


class FairPlayAdmin(admin.ModelAdmin):
    list_display = ['title','is_active']

    def has_add_permission(self, *args, **kwargs):
        return not FairPlay.objects.exists()


class ImprintAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']

    def has_add_permission(self, *args, **kwargs):
        return not Imprint.objects.exists()


class CustomerCareAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'designation', 'person_img']


admin.site.register(HeroSection, HeroSectionAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CustomerCare, CustomerCareAdmin)
admin.site.register(GeneralFAQs, GeneralFAQsAdmin)
admin.site.register(HowToRentFAQs, HowToRentFAQsAdmin)
admin.site.register(HowToListFAQs, HowToListFAQsAdmin)
admin.site.register(ObjectOwnerFAQs, ObjectOwnerFAQsAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(HowItWork, HowItWorkAdmin)
# admin.site.register(WhyHorsedCh, WhyHorsedChAdmin)
admin.site.register(SocialLinks, SocialLinksAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(DataPolicy, DataPolicyAdmin)
admin.site.register(FairPlay, FairPlayAdmin)
admin.site.register(Imprint, ImprintAdmin)
admin.site.register(Product)
admin.site.register(Category)

