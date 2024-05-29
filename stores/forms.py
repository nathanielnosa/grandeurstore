from django import forms

from . models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model =  Order
        fields = '__all__'
        exclude = ['cart','amount','subtotal','ref','payment_complete','order_status']
        widgets ={
            'order_by':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'payment_method':forms.Select(attrs={'class':'form-control'}),
        }
        