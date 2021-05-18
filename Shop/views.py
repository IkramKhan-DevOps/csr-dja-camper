import json
import urllib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.db import connection
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from Horsedch import settings
from Horsedch.bll import has_social_account, get_member
from Horsedch.models import Member, Landlord
from Landlord.models import Language, LandlordBankAccount
from Shop.forms import ProductForm, OrderCheckOutDetailsForm
from Shop.helpers import get_or_create_customer
from Shop.models import Category, Product, Order
import stripe


@login_required()
def add_product(request):
    social_account = ""
    member = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)
    category = Category.objects.all()
    if social_account:
        print(social_account)
    else:
        print("NO social account")

    if request.method == "POST":
        if "add-product" in request.POST:
            form = ProductForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                landlord = Landlord.objects.get(member__user=request.user)
                product = form.save(commit=False)
                product.landlord = landlord
                product.save()
                messages.success(request, "Action Completed Successfully!")

            else:
                messages.error(request, form.errors)

    context = {
        'categories': category,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/add-product.html", context=context)


@login_required()
def all_products(request):
    social_account = ""
    member = ""
    products = ""
    try:
        social_account = has_social_account(request.user)
    except ObjectDoesNotExist:
        member = get_member(request.user)


    try:
        query = "SELECT Shop_product.id,Shop_product.product_slug, Shop_product.product_title, Shop_product.price, Shop_product.rental_type, Shop_product.image_1, avg(Shop_order.stars_by_renter) AS stars FROM Shop_product LEFT JOIN Shop_order ON Shop_product.id=Shop_order.product_id GROUP BY Shop_product.id"
        products = Product.objects.raw(query)
    except:
        print("Error in loading products")

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # with connection.cursor() as cursor:
    #     cursor.execute(query)
    #     products = cursor.fetchall()
    # print(products)

    if request.method == "POST" and "search-product" in request.POST:
        try:
            query = "SELECT Shop_product.id,Shop_product.product_slug, Shop_product.product_title, Shop_product.price, Shop_product.rental_type, Shop_product.image_1, avg(Shop_order.stars_by_renter) AS stars FROM Shop_product LEFT JOIN Shop_order ON Shop_product.id=Shop_order.product_id WHERE Shop_product.product_title LIKE '%"+request.POST.get("product_title_search")+"' OR Shop_product.product_title LIKE '"+request.POST.get("product_title_search")+"%' GROUP BY Shop_product.id"
            print(query)
            products = Product.objects.raw(query)
        except:
            print("No product found")
            messages.info(request, "Unfortunately, we don't have your required item.")

    context = {
        'social_account': social_account,
        'member': member,
        'products': products,
    }
    return render(request, template_name="shop/products/all-products.html", context=context)


def my_products(request):
    social_account = ""
    member = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)

    products = ""
    try:
        landlord = Landlord.objects.get(member__user=request.user)
        # query = "SELECT Shop_product.id, product_title, price, rental_type, image_1, avg(stars_by_renter) AS stars FROM Shop_product left outer join Shop_order on Shop_product.id=Shop_order.product_id WHERE Shop_product.landlord_id=%s" % landlord.id
        products = Product.objects.filter(landlord=landlord)


    except:
        messages.error(request, "You don't have added any product yet.")

    context = {
        "products": products,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/products/my-products.html", context=context)


def edit_product(request, p_id):
    social_account = ""
    member = ""
    categories = ""
    try:
        social_account = has_social_account(request.user)
    except:
        member = get_member(request.user)
    product = ""
    try:
        product = Product.objects.get(id=p_id, landlord__member__user=request.user)
        categories = Category.objects.all()
    except:
        print("No product exists")
        # return to 404

    if request.method == "POST":
        product.product_title = request.POST.get("product_title")
        product.zip_code = request.POST.get("zip_code")
        product.city_name = request.POST.get("city_name")
        product.price = request.POST.get("price")
        product.rental_type = request.POST["rental_type"]
        product.brand = request.POST.get("brand")
        product.available_from = request.POST.get("available_from")
        product.hide_item = request.POST["hide_item"]
        product.product_description = request.POST.get("product_description")
        product.offer_shipping = request.POST["offer_shipping"]
        product.pick_up = request.POST["pick_up"]
        product.image_1 = request.POST["image_1"]
        product.image_2 = request.POST["image_2"]
        product.image_3 = request.POST["image_3"]
        product.image_4 = request.POST["image_4"]

        if request.POST["category_1"] != "Select":
            category_1 = request.POST["category_1"]
            messages.success(request, "Action Completed Successfully!")
        else:
            messages.error(request, "Please select product category.")
        if request.POST["category_2"] != "Select":
            category_2 = request.POST["category_2"]
        if request.POST["category_3"] != "Select":
            category_3 = request.POST["category_3"]
        product.save()

    context = {
        "product": product,
        'social_account': social_account,
        'member': member,
        'categories': categories,
    }

    return render(request, template_name="shop/products/edit-product.html", context=context)


def rate_rental_experience(request):
    return render(request, template_name="shop/reviews/rate-rental-experience.html")


# def book_product(request, p_id):


def checkout(request):
    social_account = ""
    member = ""
    product = ""
    from_date = ""
    till_date = timezone.now()
    duration_days = timezone.now()
    rent_amount = 0.0
    service_charges = 0.0
    try:
        social_account = has_social_account(request.user)
    except ObjectDoesNotExist:
        member = get_member(request.user)

    if request.method == "POST" and "book-now" in request.POST:
        try:
            product = Product.objects.get(id=request.POST.get("product_id"))
            from_date = parse_date(request.POST.get("rent_from_date"))
            till_date = parse_date(request.POST.get("rent_till_date"))
            duration_days = till_date - from_date
            if product.rental_type == "Per Day":
                rent_amount = product.price * duration_days.days
            elif product.rental_type == "Per Month":
                rent_amount = (product.price/30) * duration_days.days
            elif product.rental_type == "Per Year":
                rent_amount = (product.price/365) * duration_days.days

            service_charges = rent_amount*0.10

            print(duration_days.days)
        except:
            print("something happened in checkout")

    context = {
        'social_account': social_account,
        'member': member,
        'product': product,
        'from_date': from_date,
        'till_date': till_date,
        'duration_days': duration_days,
        'rent_amount': rent_amount,
        'service_charges': service_charges,
        'key': settings.STRIPE_PUBLISHABLE_KEY
    }

    return render(request, template_name="shop/take_on_rent/checkout.html", context=context)


def single_product_details(request, slug):
    social_account = ""
    member = ""
    product = ""
    product_reviews = ""
    total_reviews = ""
    language = ""
    try:
        social_account = has_social_account(request.user)
    except ObjectDoesNotExist:
        print("Social Account does not exists")
        member = get_member(request.user)

    try:
        product = Product.objects.get(product_slug=slug)
        product_reviews = Order.objects.filter(product=product).aggregate(Avg('stars_by_renter'))
        total_reviews = Order.objects.filter(product=product, stars_by_renter__isnull=False).count()
        language = Language.objects.get(landlord=product.landlord)
    except ObjectDoesNotExist:
        print("Product does not exists")
        # return to 404.

    context = {
        'product': product,
        'product_reviews': product_reviews,
        'total_reviews': total_reviews,
        'language': language,
        'social_account': social_account,
        'member': member,
    }
    return render(request, template_name="shop/take_on_rent/product_details.html", context=context)


def profile_reviews(request):
    return render(request, template_name="shop/reviews/reviews.html")


stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )

            # payment_intent = stripe.PaymentIntent.create(
            #     # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            #     # cancel_url=domain_url + 'cancelled/',
            #     payment_method_types=['card'],
            #     amount=1000,
            #     currency='usd',
            #     application_fee_amount=123,
            #     transfer_data={
            #         'destination': '{{CONNECTED_STRIPE_ACCOUNT_ID}}',
            #     }
            # )
            # print(payment_intent)
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class RentChargeView(View):

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        json_data = json.loads(request.body)
        product = Product.objects.filter(id=json_data['product_id']).first()
        # fee_percentage = .01 * int(product.fee)
        bank_info = LandlordBankAccount.objects.get(landlord=product.landlord)
        try:
            customer = get_or_create_customer(
                self.request.user.email,
                json_data['token'],
            )
            total_amount = float(json_data['amount'])
            service_charges = float(json_data['service_charges'])
            total_amount = total_amount - service_charges
            print("this is total amount: ",total_amount)
            charge = stripe.Charge.create(
                amount=int(json_data['amount'])*100,
                currency='usd',
                customer=customer.id,
                description=json_data['description'],
                application_fee_amount=int(service_charges)*100,
                transfer_data={
                    # 'amount': int(total_amount)*100,
                    'destination': bank_info.stripe_user_id,
                }
            )
            if charge:
                print("Charges successfully")
                form = OrderCheckOutDetailsForm(data=request.POST, files=request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    print(form.errors)
                return JsonResponse({'status': 'success'}, status=202)

        except stripe.error.StripeError as e:
            print(e)
            return JsonResponse({'status': 'error'}, status=500)



# def search_product(request):
#     if request.method == "POST":
#         products = Product.objects.filter(product_title__search=request.POST.get("product_title_search"))
#
#     context = {
#         'products': products
#     }
