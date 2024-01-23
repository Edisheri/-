from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_session_id(request, item_id):
    item = Item.objects.get(id=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cancel/'),
    )

    return JsonResponse({'session_id': session.id})

def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'item': item}
    return render(request, 'item_detail.html', context)