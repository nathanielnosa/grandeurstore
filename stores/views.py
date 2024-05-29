from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from django.contrib import messages
from django.db.models import Q

from . models import *
from . forms import CheckoutForm
# Create your views here.
def index(request):
    category = Category.objects.all()
    products = Product.objects.all().order_by('-created')[:8]
    context={
        'categorys':category,
        'products':products
    }

    return render(request, 'stores/index.html',context)

# all products
def products(request):
    products = Product.objects.all().order_by('-created')
    # pagination
    paginator = Paginator(products,6)
    page_number = request.GET.get("page")
    page_list = paginator.get_page(page_number)
    context={
        'products':products,
        'paginator':page_list
    }
    return render(request,'stores/all-product.html',context)

# detail product
def product(request,id):
    product = Product.objects.get(id=id)

    context={
        'product':product
    }
    return render(request,'stores/single-product.html',context)

# category
def category(request,id):
    category = Product.objects.all().filter(category = id)
    context={
        'categorys':category,
    }
    return render(request,'stores/category.html',context)

# add to cart
def addToCart(request,id):
    
    # get the product
    cart_product = Product.objects.get(id=id)

    # check if product is already in cart
    cart_id = request.session.get('cart_id',None)
    # get product price or discount price
    price_to_use = cart_product.discount_price if cart_product.discount_price else cart_product.price

    # check if user has a cart already
    if cart_id:
        # cart_item = Cart.objects.get(id=cart_id)
        cart_item = get_object_or_404(Cart,id=cart_id) #Cart ... CartProduct

        # assign the cart to a login user
        if request.user.is_authenticated and request.user.profile:
            cart_item.profile = request.user.profile
            cart_item.save()

        # check if a product exist
        this_product_in_cart = cart_item.cartproduct_set.filter(product=cart_product)
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity +=1
            cartproduct.subtotal += price_to_use
            cartproduct.save()
            cart_item.total += price_to_use
            cart_item.save()
            messages.success(request,'item increase in cart')
        else:
            cartproduct = CartProduct.objects.create(product = cart_product,cart=cart_item,quantity=1, subtotal= price_to_use)
            cart_item.total += price_to_use
            cart_item.save()
            messages.success(request,'a new product added to cart')
    else:
        cart_item = Cart.objects.create(total=0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(product = cart_product,cart=cart_item,quantity=1, subtotal= price_to_use)
        cart_item.total += price_to_use
        cart_item.save()
        messages.success(request,'A new item added successfully')
    return redirect('products')

# my cart
def myCart(request):
    cart_id = request.session.get('cart_id',None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)
        # assign the cart to a login user
        if request.user.is_authenticated and request.user.profile:
            cart_item.profile = request.user.profile
            cart_item.save()
    else:
        cart_item = None
    context={
        'carts':cart_item
    }
    return render(request,'stores/mycart.html',context)


# manage cart
def manageCart(request,id):
    cart_product = CartProduct.objects.get(id=id)
    price_to_use = cart_product.product.discount_price if cart_product.product.discount_price else cart_product.product.price
    cart = cart_product.cart

    action = request.GET.get('action')
    if action == 'inc':
        cart_product.quantity += 1
        cart_product.subtotal += price_to_use
        cart_product.save()
        cart.total += price_to_use
        cart.save()
        messages.success(request, 'Item increased in cart')
    elif action == 'dcr':
        cart_product.quantity -= 1
        cart_product.subtotal -= price_to_use
        cart_product.save()
        cart.total -= price_to_use
        cart.save()
        if cart_product.quantity == 0:
            cart_product.delete()
            cart.save()
        messages.success(request, 'Item increased in cart')
    return redirect('my-cart')


# checkout
def checkout(request):
    cart_id = request.session.get('cart_id',None)
    cart_item = Cart.objects.get(id=cart_id)

    form = CheckoutForm()
    # assign cart to login person and redirecting the person back to checkout
    if request.user.is_authenticated and request.user.profile:
        pass
    else:
        return redirect('/users/login/?next=/checkout/')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.cart = cart_item
            form.amount = cart_item.total
            form.subtotal = cart_item.total
            paymentmethod = form.payment_method
            del request.session['cart_id']
            form.save()

            order = form.id
            if paymentmethod == 'paystack':
                return redirect('payment', id =order)
            elif paymentmethod == 'stripe':
                pass
            elif paymentmethod == 'transfer':
                pass
    context={
        'form':form,
        'cart':cart_item
    }
    return render(request,'stores/checkout.html',context)

# make payment
def payment(request,id):
    order = Order.objects.get(id=id)
    context={
        'order':order,
        'paystack':settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request,'stores/payment.html',context)

# verify payment
def verify_payment(request:HttpRequest,ref:str)->HttpResponse:
    payment = get_object_or_404(Order,ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request,'Payment verification successful')
    else:
        messages.error(request,'Payment verification failed')
    return redirect('dashboard')


def search(request):
    get_kword = request.GET.get('kword')
    product = Product.objects.filter(Q(title__icontains=get_kword) | Q(description__icontains=get_kword))

    context = {
        'product':product
    }
    return render(request,'stores/search.html',context)