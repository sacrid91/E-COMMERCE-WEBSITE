from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse

def _cart_id(request):  #_cart_id becomes a private fn when _ is before fn name
    cart= request.session.session_key             #creates card_id from website cookies session id
    if not cart:
        cart = request.session.create()   #creates a session ID if missing 
    return cart


def add_cart(request, product_id):
    product= Product.objects.get(id=product_id) #gets the product
    try:
        cart= Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart id pressent in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )    
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product =product, cart = cart )
        cart_item.quantity += 1 #cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create( #Creates a new cart_item
            product = product,
            quantity = 1,
            cart = cart,
        )   
        cart_item.save() 
    
    return redirect('cart')   

#----
def remove_cart(request, product_id):
    try:
        product = get_object_or_404(Product,id=product_id)  # Get the product
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart
        cart_item = CartItem.objects.get(product=product, cart=cart)  # Get the cart item

        if cart_item.quantity > 1:  # If quantity is greater than 1, decrement it
            cart_item.quantity -= 1
            cart_item.save()
        else:  # If quantity is 1, remove the item from the cart
            cart_item.delete()
    except (Product.DoesNotExist, Cart.DoesNotExist, CartItem.DoesNotExist):
        pass  # Handle the error gracefully (e.g., log the error or show a message)

    return redirect('cart')  # Redirect back to the cart page
#----

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect ('cart')
    
    
def cart(request, total=0, quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2  * total ) /100
        grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass #just ignore     
       
    context = {
        'total': total,
        'quantity':quantity,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2  * total ) /100
        grand_total = total + tax
            
    except ObjectDoesNotExist:
        pass #just ignore     
       
    context = {
        'total': total,
        'quantity':quantity,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'store/checkout.html',context)