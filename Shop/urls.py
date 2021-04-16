from django.urls import path

from Shop import views

urlpatterns = [
    path('add/product/', views.add_product, name="Add Product"),
    path('', views.all_products, name="All Products"),
    path('my/products/', views.my_products, name="My Products"),
    path('rate-rental-experience/', views.rate_rental_experience, name="Rate Rental Experience"),
    path('checkout/', views.checkout, name="Checkout"),
    path('product/details/', views.single_product_details, name="Single Product"),
    path('user/profile/reviews/', views.profile_reviews, name="Profile Reviews"),

]