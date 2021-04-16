from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


class HeroSection(models.Model):
    site_title = models.CharField(max_length=200, help_text="Enter website name/title.")
    site_description = models.TextField(max_length=300, help_text="Enter website description/tag line.")
    is_active = models.BooleanField(default=False,
                                    help_text="Uncheck to hide this title from website instead of deleting.")

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"


class Box(models.Model):
    box_title = models.CharField(max_length=50, help_text="Enter box name/title.")
    box_description = models.TextField(max_length=100, help_text="Enter box description/tag line.")
    is_active = models.BooleanField(default=False,
                                    help_text="Uncheck to hide this title from website instead of deleting.")

    def __str__(self):
        return self.box_title

    class Meta:
        verbose_name = "Boxes Section"
        verbose_name_plural = "Boxes Section"


class AboutUs(models.Model):
    heading = models.CharField(max_length=100, help_text="Enter about us heading.")
    sub_heading = models.CharField(max_length=150, help_text="Enter about us sub-heading.")
    description = models.TextField(max_length=1000, help_text="Enter about us description.")
    is_active = models.BooleanField(default=False,
                                    help_text="Uncheck to hide this title from website instead of deleting.")

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name = "About us Section"
        verbose_name_plural = "About us Section"


class Team(models.Model):
    person_img = models.ImageField(upload_to="images/team", null=True, blank=True,
                                   help_text="Please select an image of the person.")
    full_name = models.CharField(max_length=50, help_text="Enter person name.")
    designation = models.CharField(max_length=50, help_text="Enter person's designation.")
    facebook_link = models.URLField(max_length=200, help_text="Please enter facebook profile/page URL.")
    instagram_link = models.URLField(max_length=200, help_text="Please enter instagram profile URL.")
    email_address = models.EmailField(help_text="Please enter person's email address")

    def __str__(self):
        return self.designation

    class Meta:
        verbose_name = "Teams Section"
        verbose_name_plural = "Teams Section"


class GeneralFAQs(models.Model):
    question = models.CharField(max_length=100, help_text="Enter question here.")
    answer = models.TextField(max_length=300, help_text="Enter question here.")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "General FAQs"
        verbose_name_plural = "General FAQs"


class HowToRentFAQs(models.Model):
    question = models.CharField(max_length=100, help_text="Enter question here.")
    answer = models.TextField(max_length=300, help_text="Enter question here.")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "How to rent FAQs"
        verbose_name_plural = "How to rent FAQs"


class HowToListFAQs(models.Model):
    question = models.CharField(max_length=100, help_text="Enter question here.")
    answer = models.TextField(max_length=300, help_text="Enter question here.")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "How to list FAQs"
        verbose_name_plural = "How to list FAQs"


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
                                    help_text="Please enter company phone number here.")

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


class Member(models.Model):
    ROLE_CHOICES = [
        ("LND", "Landlord"),
        ("RNR", "Renter"),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    street_address = models.TextField(max_length=200, null=True, blank=True)
    house_number = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    profile_status = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="images/users/", null=True, blank=True, default="no-image-icon.png")
    self_description = models.TextField(max_length=500, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email_address)

    class Meta:
        verbose_name = "Members"
        verbose_name_plural = "Members"


class Landlord(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member.email_address)

    class Meta:
        verbose_name = "Landlords"
        verbose_name_plural = "Landlords"


class Renter(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member.email_address)

    class Meta:
        verbose_name = "Renters"
        verbose_name_plural = "Renters"
