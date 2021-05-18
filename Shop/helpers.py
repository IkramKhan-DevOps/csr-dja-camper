import stripe

from Horsedch import settings


def get_or_create_customer(email, token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    connected_customers = stripe.Customer.list()
    for customer in connected_customers:
        if customer.email == email:
            print(f'{email} found')
            return customer
    print(f'{email} created')
    return stripe.Customer.create(
        email=email,
        source=token,
    )