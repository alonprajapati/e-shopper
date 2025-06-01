from .models import *
from .models import CustomUserModel
from .forms import ProfileForm

from core.models import Order

from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

import re
# Create your views here.
def register(request):
    if "register" in request.POST:

        fname=request.POST.get('first_name')
        lname=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone = request.POST.get('phone')
        street_code = request.POST.get('street_code')
        password1=request.POST.get('password1')

        if password==password1:
            if CustomUserModel.objects.filter(username=username).exists():
                messages.error(request,'username already exists')
                return redirect('register')
            if CustomUserModel.objects.filter(email=email).exists():
                messages.error(request,'email already exists')
                return redirect('register')
            
            if not re.search(r"[A-Z]",password):
                messages.error(request,'your password must contain at least one upper character!!')
                return redirect('register')
            if not re.search(r"\d",password):
                messages.error(request,'your password must contain at least one digit!!')
                return redirect('register')               
            if not re.search(r"\W",password):
                messages.error(request,'your password must contain at least one special character!!')
                return redirect('register')

            try:
                validate_password(password)                
                CustomUserModel.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password,phone=phone,street_address=street_code)
                messages.success(request,"data registered successfully!!!")
                return redirect('log_in')
            except ValidationError as e:
                for i in e.messages:
                    messages.error(request.i)
                return redirect('register')
            
        else:
            messages.error(request,"password doesnot match!!!!!")
            return redirect('register')
    
    return render(request,'auth/login.html')

def log_in(request):
    if 'login' in request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me')

        if not CustomUserModel.objects.filter(username=username).exists():
            messages.error(request,'username is not register yet!!!')
            return redirect('log_in')
        
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(12000000)
            else:
                request.session.set_expiry(0)

            next=request.POST.get('next','')
            return redirect(next if next else 'index')
        else:
            messages.error(request,'incorrect password')
            return redirect('log_in')
    
    next=request.GET.get('next','')
    return render(request,'auth/login.html',{'next':next})

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        
    return render(request,'profile/change_password.html',{'form':form})

# ------profile-----
@login_required(login_url='log_in')
def profile(request):
    return render(request,'profile/profile.html')

@login_required(login_url='log_in')
def update_profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    form=ProfileForm(instance=profile)

    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context={
        'form':form,
        'user':request.user,
        'profile':request.user.profile,

    }
    return render(request,'profile/update_profile.html',context)

def my_order(request):
    if request.method=='POST':
        phone=request.POST['phone']
        address=request.POST['address']
        cart=request.session.get('cart')
        uid=request.session.get("_auth_user_id")
        user=CustomUserModel.objects.get(id=uid)

        for i in cart:
            product=cart[i]['name']
            quantity=cart[i]['quantity']
            price=cart[i]['price']
            total=quantity*float(price)
            image=cart[i]['image']

            myorder=Order(product=product,user=user,quantity=quantity,price=price,total=total,image=image,phone=phone,address=address)
            myorder.save()

        request.session['cart']={}

    uid=request.session.get("_auth_user_id")
    user=CustomUserModel.objects.get(id=uid)
    myorder=Order.objects.filter(user=user)

    return render(request,'profile/my_order.html',{'myorder':myorder})