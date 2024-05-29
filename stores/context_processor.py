from . models import Category, CartProduct,Cart

def category(request):
    categorys = Category.objects.all()
    context={
        'category':categorys
    }
    return context


def cartproducts(request):
    cart_id = request.session.get('cart_id', None)
    cart_count = 0  # Initialize cart count to 0
    
    if cart_id:
        try:
            cart_item = Cart.objects.get(id=cart_id)
            cart_count =cart_item.cartproduct_set.all().count()
            #cart_count =  CartProduct.objects.filter(cart=cart_item).count()  # Count the number of products in the cart
            if request.user.is_authenticated and request.user.profile:
                cart_item.profile = request.user.profile
                cart_item.save()
        except Cart.DoesNotExist:
            cart_item = None
    
    context = {
        'cart': cart_count
    }
    
    return context
