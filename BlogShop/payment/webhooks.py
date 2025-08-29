from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings
from django.http import HttpResponse
from .models import BalanceTransaction, Balance, BuyProductTransaction
from decimal import Decimal

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header, 
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            user=int(session.metadata.get('user_id'))
            if session.metadata.get('type') == 'balance_topup':
                transaction = get_object_or_404(BalanceTransaction, id=session.client_reference_id, user=user)
                transaction.paid = True
                transaction.stripe_id = session.payment_intent
                transaction.save()
                balance = get_object_or_404(Balance, user=user)
                balance.balance += Decimal(session.amount_total / Decimal(100))
                balance.save()
            elif session.metadata.get('type') == 'product_purchase':
                transaction = get_object_or_404(BuyProductTransaction, id=session.client_reference_id, user=user)
                transaction.paid = True
                transaction.stripe_id = session.payment_intent
                transaction.save()
                transaction.product.quantity -= transaction.quantity
                transaction.product.save()
                balance = get_object_or_404(Balance, user=user)
                balance.balance = 0
                seller = get_object_or_404(Balance, user=transaction.product.seller)
                seller.balance += transaction.get_cost()
                balance.save()
                seller.save()
    return HttpResponse(status=200)