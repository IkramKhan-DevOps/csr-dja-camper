from django.shortcuts import render


def index_view(request):
    return render(request, template_name="index.html")


def sign_up_view(request):
    return render(request, template_name="authentication/signup_using_email.html")