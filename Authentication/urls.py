from django.urls import path

from Authentication import views

urlpatterns = [
    path('edit/profile/', views.edit_profile, name="Edit Profile"),
    path('my/account/', views.my_account, name="My Account"),
    path('select/role/', views.choose_role, name="choose_role"),
    path('select/role/<str:role>/', views.update_member_role, name="update_member_role"),
]
