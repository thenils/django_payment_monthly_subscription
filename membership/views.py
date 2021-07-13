from django.shortcuts import render
from django.conf import settings
from .models import Invoice, Membership, UserMembership
from datetime import datetime, timedelta
# from django.http import HttpResponse
# Create your views here.
import stripe


def Home(request):
    return render(request, 'membership/home.html')


def Plans(request):
    plans = Membership.objects.all()

    ctx = {
        'plans': plans
    }

    return render(request, 'membership/select_plan.html', ctx)


def get_selected_membership(request, slug):
    membership_qs = Membership.objects.filter(slug=slug)

    if membership_qs.exists():
        return membership_qs.first()


def checkout(request, slug):
    membership_qs = get_selected_membership(request, slug)
    print(membership_qs.membership_type)
    # amprint(membership.price)

    membership = membership_qs.membership_type
    amount = membership_qs.price
    stripe.api_key = settings.STRIPE_SECRET_KEY

    ctx = {
        'membership': membership,
        'amount': amount,
    }
    if request.method == 'POST':
        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='inr',
            description=membership,
        )

        print(charge)
        if charge['paid'] == True:
            user = request.user
            is_subscribed = True
            membership = membership_qs
            expiry_date = datetime.now() + timedelta(28)

            UserMembership.objects.create(
                user=user, is_subscribed=is_subscribed, membership=membership, expiry_date=expiry_date)

            amount = charge['amount']/100
            txn_id = charge['id']
            Invoice.objects.create(
                user=user, user_membership=membership, price=amount, txn_id=txn_id)

            return render(request, 'membership/success.html', ctx)

        else:
            return render(request, 'membership/cancel.html')
    return render(request, 'membership/checkout.html', ctx)
