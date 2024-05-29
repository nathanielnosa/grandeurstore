from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from . forms import UpdateProfile, UserProfile
from stores.models import Order
# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    formShow = UserProfile
    if request.method == 'POST':
        form = UserProfile(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            print(f'::user::{password}')
            if password != password2:
                messages.warning(request,'password does not match')
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.warning(request,'email already exist')
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.warning(request,'username already exist')
                return redirect('register')
                
            user = User.objects.create_user(username,email,password)
            print(f'::user::{user}')
            formTemp = form.save(commit=False)
            formTemp.user = user
            formTemp.save()
            messages.success(request,'register successful')
            return redirect('login')
        if 'next' in request.GET:
                next_url =  request.GET.get('next')
                return redirect(next_url)
    context={
        'form':formShow
    }
    return render(request,'users/register.html',context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']

        user = authenticate(username = username, password = password)
        if user :
            login(request,user)
            messages.success(request,'Login successful')

            if 'next' in request.GET:
                next_url =  request.GET.get('next')
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.warning(request,'Username/Password not correct')
            return redirect('login')

    return render(request,'users/login.html')


def logoutuser(request):
    logout(request)
    messages.success(request,'Logout successful')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    profile = request.user.profile
    order = Order.objects.filter(cart__profile = profile).prefetch_related('cart__cartproduct_set__product')
    context={
        'profile':profile,
        'order':order
    }
    return render(request,'users/dashboard.html',context)

@login_required(login_url='login')
def updateprofile(request):
    profile = request.user.profile
    form = UpdateProfile(instance=profile)
    if request.method == 'POST':
        form = UpdateProfile(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            # user = request.user
            user = User.objects.get(username=request.user)
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            form.save()
            return redirect('dashboard')

    context={
        'profile':profile,
        'form':form,
        'show_profile_form': True,
    }
    return render(request,'users/updateprofile.html',context)

