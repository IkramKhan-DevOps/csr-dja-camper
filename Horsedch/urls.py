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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from Horsedch import views, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="Home"),
    path('accounts/signup/', views.sign_up_view, name="Sign Up"),
    path('conditions/', views.conditions, name="Conditions"),
    path('data-policy/', views.data_policy, name="Data Policy"),
    path('fairplay/', views.fairplay, name="Fair Play"),
    path('imprint/', views.imprint, name="Imprint"),
    path('about-us/', views.about_us, name="About Us"),
    path('faqs/', views.faqs, name="FAQs"),
    path('faqs/object-owners/', views.faqs_object_owners, name="FAQs_Object_Owners"),
    path('partners/', views.our_partners, name="Partners"),

    path('accounts/login/', views.login, name="Login"),
    # path('logout/', views.auth_logout, name="Logout"),

    # url(r'^google-login/$', views.login_via_google, name="login_via_google"),
    # url(r'^facebook-login/$', views.login_via_facebook, name="login_via_facebook"),

    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name="Logout"),

    path('shop/', include('Shop.urls')),
    path('auth/', include('Authentication.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
