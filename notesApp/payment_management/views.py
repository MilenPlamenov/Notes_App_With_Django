from django.shortcuts import render, redirect

import stripe
from django.urls import reverse

stripe.api_key = "sk_test_51Keh4BGrEyPil1dZSZJc2XhTcMNhYAIWEGCDpuIh0zPycac3P7bggBSJqHCRuYIgMnkg4Mb1eJ97zP94XKol3tpS00rwtA50Ks"


'''

 Using stripe to make simple payment system
 Doesn't save anything in the database to protect the user information 

'''


def charge(request):
    if not request.user.is_authenticated:
        return redirect('create profile')
    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        customer = stripe.Customer.create(
            name=request.user.username,
            source=request.POST['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='bgn',
            description='donation',
        )
        return redirect(reverse('success message', args=[amount]))
    return render(request, 'payments/card_payments.html')


def success_message(request, args):
    amount = args
    context = {
        'amount': amount
    }
    return render(request, 'payments/success_message_payment.html', context)
