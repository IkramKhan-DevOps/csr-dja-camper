from django.db import models
from ckeditor.fields import RichTextField


class HowItWork(models.Model):
    picture = models.ImageField(upload_to="images/how_it_work", null=True, blank=True,
                                help_text="Please select an image/icon.")
    title = models.CharField(max_length=200, null=True, blank=True, help_text="Please provide a title.")
    description = models.TextField(max_length=300, null=True, blank=True, help_text="Please provide description.")
    is_active = models.BooleanField(default=False,
                                    help_text="Uncheck to hide this title from website instead of deleting.")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "How It Works Section"
        verbose_name_plural = "How It Works Section"


class WhyHorsedCh(models.Model):
    picture = models.ImageField(upload_to="images/how_it_work", null=True, blank=True,
                                help_text="Please select an image/icon.")
    title = models.CharField(max_length=200, null=True, blank=True, help_text="Please provide a title.")
    description = models.TextField(max_length=300, null=True, blank=True, help_text="Please provide description.")
    is_active = models.BooleanField(default=False,
                                    help_text="Uncheck to hide this title from website instead of deleting.")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Why Horsed.ch Section"
        verbose_name_plural = "Why Horsed.ch Section"


class SocialLinks(models.Model):
    facebook = models.URLField(max_length=200, help_text="Please enter facebook profile/page URL.")
    instagram = models.URLField(max_length=200, help_text="Please enter instagram profile URL.")
    twitter = models.URLField(max_length=200, help_text="Please enter twitter page URL.")
    is_active = models.BooleanField(default=False, help_text="Uncheck to hide this link from website")

    def __str__(self):
        return self.facebook

    class Meta:
        verbose_name = "Social Media Links"
        verbose_name_plural = "Social Media Links"


class ContactInformation(models.Model):
    building_name = models.CharField(max_length=200, null=True, blank=True,
                                     help_text="Please enter building name here.")
    street = models.CharField(max_length=200, null=True, blank=True, help_text="Please enter street here.")
    post_code = models.CharField(max_length=50, null=True, blank=True, help_text="Please enter post code/town here.")
    email_address = models.EmailField(max_length=200, null=True, blank=True,
                                      help_text="Please enter company email address here.")
    phone_number = models.CharField(max_length=50, null=True, blank=True,
                                    help_text="Please enter comapny phone number here.")

    def __str__(self):
        return self.building_name

    class Meta:
        verbose_name = "Company Contact Information"
        verbose_name_plural = "Company Contact Information"


class Condition(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField()
    is_active = models.BooleanField(default=False, help_text="Uncheck to hide this from website")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Terms & Condition"
        verbose_name_plural = "Terms & Conditions"


class DataPolicy(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField()
    is_active = models.BooleanField(default=False, help_text="Uncheck to hide this from website")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Data Policy"
        verbose_name_plural = "Data Policy"


class FairPlay(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField()
    is_active = models.BooleanField(default=False, help_text="Uncheck to hide this from website")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Fair Play"
        verbose_name_plural = "Fair Play"


class Imprint(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField()
    is_active = models.BooleanField(default=False, help_text="Uncheck to hide this from website")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Imprint"
        verbose_name_plural = "Imprint"
