from django.urls import path

from Shop import views
from Shop.views import RentChargeView

urlpatterns = [
    path('add/product/', views.add_product, name="Add Product"),
    path('edit/<int:p_id>/product/', views.edit_product, name="edit_my_product"),
    path('', views.all_products, name="All Products"),
    path('my-products/', views.my_products, name="My Products"),
    path('rate-rental-experience/', views.rate_rental_experience, name="Rate Rental Experience"),
    path('checkout/', views.checkout, name="Checkout"),
    path('<slug:slug>/details/', views.single_product_details, name="single_product_details"),
    path('user/profile/reviews/', views.profile_reviews, name="Profile Reviews"),
    path('checkout/', views.checkout, name="checkout"),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('charge/', RentChargeView.as_view(), name='charge'),
]
