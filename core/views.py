from django.shortcuts import render, get_object_or_404
from item.models import Category, Item
from cart.models import Cart, CartItem

def search_products(request):
    query = request.GET.get("q", "")
    products = Item.objects.filter(name__icontains=query)[:5] if query else []
    context = {
        "products": products,
        'input_value':query,
        }
    return render(request, "core/search_results.html", context)


def detail_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    related_items = Item.objects.filter(category=item.category).exclude(id=item_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        added_items = [cart_item.item for cart_item in cart_items]
    else:
        added_items = []
        cart_items = []
    
    context = {
        "item":item,
        'related_items':related_items,
        'category':item.category.name,
        'added_items':added_items,
    }
    return render(request, 'core/detail.html', context)

def home_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        added_items = [cart_item.item for cart_item in cart_items]    
    else:
        added_items = []
        cart_items = []
        None
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    
    context = {
        'items':items,
        'categories':categories,
        'added_items':added_items,
        'cart_items':cart_items,
    }
    
    return render(request, 'core/home.html', context)