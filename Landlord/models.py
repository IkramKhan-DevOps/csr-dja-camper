from django.db import models

from Horsedch.models import Landlord


class Language(models.Model):
    dutch = models.BooleanField(default=False, null=True, blank=True)
    french = models.BooleanField(default=False, null=True, blank=True)
    italian = models.BooleanField(default=False, null=True, blank=True)
    english = models.BooleanField(default=False, null=True, blank=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Languages"
        verbose_name_plural = "Languages"


class SocialMediaLinks(models.Model):
    facebook = models.URLField(max_length=200, help_text="Please enter facebook profile URL.")
    instagram = models.URLField(max_length=200, help_text="Please enter instagram profile URL.")
    twitter = models.URLField(max_length=200, help_text="Please enter twitter profile URL.")
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Social Media Links"
        verbose_name_plural = "Social Media Links"


class LandlordBankAccount(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    street_address = models.TextField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    IBAN = models.CharField(max_length=50, null=True, blank=True)
    BIC = models.CharField(max_length=50, null=True, blank=True)

    stripe_user_id = models.CharField(max_length=255, blank=True)
    stripe_access_token = models.CharField(max_length=255, blank=True)

    landlord = models.OneToOneField(Landlord, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.landlord.member.email_address)

    class Meta:
        verbose_name = "Landlord Bank Account Details"
        verbose_name_plural = "Landlord Bank Account Details"
