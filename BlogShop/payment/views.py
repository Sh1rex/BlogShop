from django.shortcuts import render, redirect
from .forms import TopUpBalanceForm
from django.contrib.auth.decorators import login_required
from .models import BalanceTransiction
import stripe 
from django.conf import settings
from django.urls import reverse
import decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def topupbalanceview(request):
    if request.method == 'POST':
        form = TopUpBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction = BalanceTransiction.objects.create(user=request.user, amount=amount)
            success_url = request.build_absolute_uri(
                reverse('payment:success')
                )
            cancel_url = request.build_absolute_uri(
                reverse('payment:cancel')
            )
            session_data = {
                'mode':'payment',
                'success_url': success_url,
                'cancel_url': cancel_url,
                'client_reference_id': transaction.id,
                'metadata': {
                    'user_id': request.user.id,
                },
                'line_items':[{
                    'quantity': 1,
                    'price_data':{
                        'unit_amount': int(decimal.Decimal(amount)*100),
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Top Up Balance',
                        }
                    }
                }]
            }
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)
    form = TopUpBalanceForm()
    return render(request, 'payment/topupbalance.html',{
        'form': form,
    })

def success(request):
    return render(request, 'payment/success.html')

def cancel(request):
    return render(request, 'payment/cancel.html')