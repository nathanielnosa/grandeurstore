from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('product/<str:id>/',views.product,name='product'),
    path('products/',views.products,name='products'),
    path('category/<str:id>/',views.category,name='category'),
    path('add-to-cart/<str:id>/',views.addToCart,name='add-to-cart'),
    path('my-cart/',views.myCart,name='my-cart'),
    path('manage-cart/<str:id>/',views.manageCart,name='manage-cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('search/',views.search,name='search'),
    path('payment/<str:id>/',views.payment,name='payment'),
    path('<str:ref>/',views.verify_payment,name='verify-payment'),
]