from django.shortcuts import render


def index_view(request):
    return render(request, template_name="index.html")


def sign_up_view(request):
    return render(request, template_name="authentication/signup_using_email.html")


def add_product(request):
    return render(request, template_name="products/add-product.html")


def all_products(request):
    return render(request, template_name="products/all-products.html")


def my_products(request):
    return render(request, template_name="products/my-products.html")


def edit_profile(request):
    return render(request, template_name="profile/edit-profile.html")


def my_account(request):
    return render(request, template_name="profile/my-account.html")


def rate_rental_experience(request):
    return render(request, template_name="reviews/rate-rental-experience.html")


def profile_reviews(request):
    return render(request, template_name="reviews/reviews.html")


def conditions(request):
    return render(request, template_name="site_pages/conditions.html")


def data_policy(request):
    return render(request, template_name="site_pages/data-policy.html")


def fairplay(request):
    return render(request, template_name="site_pages/fairplay.html")


def imprint(request):
    return render(request, template_name="site_pages/imprint.html")


def checkout(request):
    return render(request, template_name="take_on_rent/checkout.html")


def single_product_details(request):
    return render(request, template_name="take_on_rent/product_details.html")


def info_page(request):
    return render(request, template_name="info.html")
