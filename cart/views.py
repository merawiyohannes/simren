from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from item.models import Item
from . forms import CheckOutForm
from .models import CheckOutOrder
from django.urls import reverse
from django.db.models import F
import uuid
from time import strftime
from .models import CheckOutItem, CheckOutOrder
from django.conf import settings
import requests

DATE = strftime("%B %d,%Y")
TIME = strftime('%I:%M:%S')

def chapa_notification(request):
    return render(request, 'cart/notification.html')

def order_number_generate():
    return str(uuid.uuid4())[:6].upper()

def chapa_payment(request, order_id, total):
    order = get_object_or_404(CheckOutOrder, id=order_id)
    tx_ref = order.order_number
    data = {
        'amount': float(total),
        'currency': 'ETB',
        'email': order.email or 'example@gmail.com',
        'first_name': order.name or 'Customer',
        'phone_number': order.phone or '',
        'tx_ref': tx_ref,
        'callback_url': request.build_absolute_uri(reverse('notification')),
        'return_url': request.build_absolute_uri(reverse('confirm_checkout', args=[order.id])),
        'customization': {
            'title': f'Order_No {order.order_number}',
            'description': 'Thanks for shopping with us.'
        }
    }
    
    headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
    chapa_url = "https://api.chapa.co/v1/transaction/initialize"
    response = requests.post(chapa_url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(response.json())
        payment_url = response.json()['data']['checkout_url']
        return redirect(payment_url)
    else:
        error_url = response.json()['data']
        print(error_url)
        print(f'the url is {response.json()}')
        return redirect('notification')


def confirm_checkout(request, order_id):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = 0
    order = get_object_or_404(CheckOutOrder, id=order_id)
    checkout_items = []
    for cart_item in cart_items:
        item = cart_item.item
        quantity = cart_item.quantity
        Item.objects.filter(id=item.id).update(quantity=F('quantity') - quantity)
        subtotal = item.price * quantity
        total += subtotal 
        checkout_items.append(CheckOutItem.objects.create(
            order=order,
            item =item,
            quantity = quantity,
            subtotal = subtotal
        ))
        remove_cart(request, item.id)
    CheckOutOrder.objects.filter(id=order_id).update(is_paid=True)
    context = {
        "checkout_items":checkout_items,
        "total":total,
        "date":DATE,
        "time":TIME,
        'order':order,
    }
    
    return render(request, 'cart/confirm.html', context)

def check_out(request):
    checkout_items = []
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = 0
    
    
    for item in cart_items:
        quantity = item.quantity
        subtotal = item.item.price * float(quantity)
        total += subtotal
        checkout_items.append({
            "item":item,
            "quantity":quantity,
            "subtotal":subtotal,
        })
        
    form = CheckOutForm()
    if request.method == "POST":
        if 'quick_checkout' in request.POST:
            order = CheckOutOrder.objects.create(order_number=order_number_generate(), created_by=request.user)
            return redirect(reverse('chapa_view', args=[order.id, total]))
        form = CheckOutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_number= order_number_generate()
            order.created_by=request.user
            order.save()
            return redirect(reverse('chapa_view', args=[order.id, total]))
        else:
            form = CheckOutForm()
            return

    context = {
        'checkout_items':checkout_items,
        'total':total,
        'form':form 
    }
    
    return render(request, 'cart/checkout.html',context)

def partial_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total =0
    for cart_item in cart_items:
       cart_item.sub_total = float(cart_item.quantity) * cart_item.item.price 
       total += cart_item.sub_total
    context = {
        'cart_items':cart_items,
        'total':total
    }
    return render(request, 'cart/partial.html', context)

def cart_items_count(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        count = len(CartItem.objects.filter(cart=cart))
    else:
        count = 0
    return HttpResponse(count)

@login_required
def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        cart_items = []
    total =0
    for cart_item in cart_items:
       cart_item.sub_total = float(cart_item.quantity) * cart_item.item.price 
       total += cart_item.sub_total
    context = {
        'cart_items':cart_items,
        'total':total
    }
    return render(request, 'cart/cart_view.html', context)

@login_required
def add_to_cart(request, item_id):
    cart, cart_created = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item, cart_item_created = CartItem.objects.get_or_create(cart=cart, item=item)
    cart_item.save()
    return HttpResponse(status=204, headers={'HX-Trigger':'cartUpdated'})
    
    
def increase_view(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    if cart_item.quantity < item.quantity:
        cart_item.quantity += 1
        cart_item.save()
    else:
        return HttpResponse(status=204, headers={'HX-Trigger':'maxItem'})
    return partial_view(request)
        
def decrese_view(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        return HttpResponse(status=204, headers={'HX-Trigger':'minItem'})
    return partial_view(request)

def remove_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(cart=cart, item=item)
    cart_item.delete()
    return partial_view(request)