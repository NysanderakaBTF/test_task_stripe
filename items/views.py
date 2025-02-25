from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
import stripe

from items.models import Item, Order


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
          # The URL of your payment completion page
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
    
def success(request):
    return render(request, 'success.html')
    

def buy_order(request, id):
    # Получаем заказ
    order = get_object_or_404(Order, id=id)
    currency = order.items.first().currency
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Формируем список элементов для Checkout
    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),  # Цена в центах
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
  
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.items.first().currency
    return render(request, 'order.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })