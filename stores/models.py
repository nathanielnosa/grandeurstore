import secrets
import uuid
from django.db import models
from . paystack import Paystack
from users.models import Profile
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.title}'
    
class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    discount_price = models.PositiveBigIntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main = models.ImageField(upload_to='product')
    photo1 = models.ImageField(upload_to='product',blank=True,null=True)
    photo2 = models.ImageField(upload_to='product',blank=True,null=True)
    photo3 = models.ImageField(upload_to='product',blank=True,null=True)
    photo4 = models.ImageField(upload_to='product',blank=True,null=True)
    delivery_date = models.CharField(max_length=50)
    return_policy = models.TextField()
    product_id = models.UUIDField(unique=True,default=uuid.uuid4)
    in_stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = uuid.uuid4()
        super().save(*args, **kwargs)

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f'Cart - {self.total}'
   
class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart - {self.cart.id}'

ORDER_STATUS=(
    ('pending','pending'),
    ('complete','complete'),
    ('cancelled','cancelled'),
)
PAYMENT_METHOD=(
    ('paystack','paystack'),
    ('transfer','transfer'),
)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    order_by = models.CharField(max_length=50)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, null=True, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, null=True, default='paystack')
    payment_complete = models.BooleanField(default=False,null=True)
    ref = models.CharField(max_length=255,null=True)
    
    def __str__(self):
        return f'{self.amount} ::: {str(self.id)}'
    
    # generate ref
    def save(self,*args,**kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)

    # amount
    def amount_value(self)->int:
        return self.amount * 100
    
    # verify payment
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref,self.amount)
        if status:
            if result['amount'] /100 == self.amount:
                self.payment_complete = True
                self.order_status = 'complete'
                self.save()
            
            # Reduce stock for each product in the cart
                cart_products = self.cart.cartproduct_set.all()
                for cart_product in cart_products:
                    cart_product.product.in_stock -= cart_product.quantity
                    cart_product.product.save()
        if self.payment_complete:
            return True
        return False


    


