"""Horsedch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from Horsedch import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="Home"),
    path('accounts/signup/', views.sign_up_view, name="Sign Up"),
    path('add/product/', views.add_product, name="Add Product"),
    path('all/products/', views.all_products, name="All Products"),
    path('my/products/', views.my_products, name="My Products"),
    path('edit/profile/', views.edit_profile, name="Edit Profile"),
    path('my/account/', views.my_account, name="My Account"),
    path('rate-rental-experience/', views.rate_rental_experience, name="Rate Rental Experience"),
    path('user/profile/reviews/', views.profile_reviews, name="Profile Reviews"),
    path('conditions/', views.conditions, name="Conditions"),
    path('data-policy/', views.data_policy, name="Data Policy"),
    path('fairplay/', views.fairplay, name="Fair Play"),
    path('imprint/', views.imprint, name="Imprint"),
    path('checkout/', views.checkout, name="Checkout"),
    path('product/details/', views.single_product_details, name="Single Product"),
    path('info/', views.info_page, name="Info")

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)