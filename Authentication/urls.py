from django.contrib.auth.views import LogoutView
from django.urls import path

from Authentication import views
from Authentication.views import StripeAuthorizeView, StripeAuthorizeCallbackView

urlpatterns = [
    # path('accounts/login/', views.login, name="Login"),
    #  path('logout/', auth_views.auth_logout, name="Logout"),
    # path('accounts/signup/', views.sign_up_with_email, name="Sign Up"),
    # path('logout', LogoutView.as_view(), name="Logout"),
    path('edit/profile/', views.edit_profile, name="Edit Profile"),
    path('my/account/', views.my_account, name="My Account"),
    path('select/role/', views.choose_role, name="choose_role"),
    path('select/role/<str:role>/', views.update_member_role, name="update_member_role"),
    path('switch-to-landlord/', views.switch_to_landlord, name="switch_to_landlord"),
    path('switch-to-renter/', views.switch_to_renter, name="switch_to_renter"),
    path('authorize/', StripeAuthorizeView.as_view(), name='authorize'),
    path('oauth/callback/', StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
]
