from django.shortcuts import render, redirect, get_object_or_404
from .forms import TopUpBalanceForm, BuyProductTransactionForm
from django.contrib.auth.decorators import login_required
from .models import BalanceTransaction, BuyProductTransaction, Balance
from blog.models import Post
import stripe 
from django.conf import settings
from django.urls import reverse
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def balancetransactioncheckoutsession(request):
    if request.method == 'POST':
        form = TopUpBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction = BalanceTransaction.objects.create(user=request.user, amount=amount)
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
                    'type': 'balance_topup',
                },
                'line_items':[{
                    'quantity': 1,
                    'price_data':{
                        'unit_amount': int(Decimal(amount)*100),
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

@login_required
def purchaseproduct(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = BuyProductTransactionForm(request.POST, quantity_max=post.quantity)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.product = post
            transaction.save()
            return redirect(reverse('payment:confirmpurchase', args=[transaction.id]))
    else:
        form = BuyProductTransactionForm(quantity_max=post.quantity)
        return render(request, 'payment/purchaseproduct.html', {
            'product': post,
            'form': form,
        })

@login_required
def confirmpurchase(request, id=None):
    transaction = get_object_or_404(BuyProductTransaction, id=id)
    if request.method == 'POST':
        totalprice = transaction.get_cost()
        balance = get_object_or_404(Balance, user=request.user)
        if balance.balance >= totalprice:
            seller = get_object_or_404(Balance, user=transaction.product.seller)
            balance.balance -= totalprice
            seller.balance += totalprice
            transaction.paid = True 
            transaction.product.quantity -= transaction.quantity
            transaction.product.save()
            transaction.save()
            balance.save()
            seller.save()
            return render(request, 'payment/success.html')
        else:
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
                    'type': 'product_purchase',
                },
                'line_items':[{
                    'quantity': 1,
                    'price_data':{
                        'unit_amount': int(Decimal(totalprice - balance.balance)*100),
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Purchase product',
                        }
                    }
                }]
            }
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)
    else:
        return render(request, 'payment/confirmpurchase.html', {
            'transaction': transaction,
        })

@login_required 
def orders(request):
    orders = BuyProductTransaction.objects.filter(product__seller=request.user, paid=True)
    return render(request, 'payment/orders.html',{
        'orders': orders,
    })

@login_required
def purchases(request):
    purchases = BuyProductTransaction.objects.filter(user=request.user, paid=True)
    return render(request, 'payment/purchases.html',{
        'purchases': purchases,
    })