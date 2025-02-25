from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import stripe

from items.models import Item, Order


def buy_item_intent(request, id):
    item = get_object_or_404(Item, pk=id)
    try:
        
        # Настраиваем секретный ключ Stripe в зависимости от валюты товара
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Создаем PaymentIntent для одного товара
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100), 
            currency=item.currency,        
            payment_method_types=['card'],  
        )
        
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        print(e)
        return HttpResponse(content=str(e), status=400)
    
def buy_item(request, id):
    item = get_object_or_404(Item, pk=id)
    try:
        session = stripe.checkout.Session.create(
          line_items=[
            {
              "price_data": {
                "currency": item.currency,
                "product_data": {"name": item.name},
                "unit_amount": int(item.price*100),
              },
              "quantity": 1,
            },
          ],
          mode="payment",
          ui_mode="embedded",
          return_url="http://localhost:8000/success"
        )
        return JsonResponse({'session_id': session.id})
    except Exception as e:
        print(e)
        return HttpResponse(content=str(e), status=400)


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
    
def item_detail_intent(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_intent.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
    
def success(request):
    return render(request, 'success.html')
    

def buy_order(request, id):
    # Получаем заказ
    order = get_object_or_404(Order, id=id)
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  
            },
            'quantity': 1
        })

    # Создаем Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        ui_mode='embedded',
        return_url='http://localhost:8000/success',
        discounts=[{
            'coupon': discount.stripe_coupon_id
        } for discount in order.discounts.all() if discount.stripe_coupon_id],
    )

    return JsonResponse({'session_id': session.id})


def buy_order_intent(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.get_currency()
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    total_amount = int(order.total_price * 100)
    
    intent = stripe.PaymentIntent.create(
        amount=total_amount,            
        currency=currency,             
        payment_method_types=['card'],  
    )
    
    return JsonResponse({'client_secret': intent.client_secret})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.items.first().currency
    return render(request, 'order.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })
    
def order_detail_intent(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.items.first().currency
    return render(request, 'order_intent.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })