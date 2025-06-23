from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer,Adress
from orders.models import Order,Shipping,payment
from products.models import products,Catogaries

# Create your views here.
def show_page(request):
    feuterd_products = products.objects.filter(isfetuerd=True).order_by('-created_at')[:5]
    catagories=Catogaries.objects.all()
    print(catagories)
    context = {
        'feuterd_products': feuterd_products,
        'catagories':catagories
    }
    return render(request,'index.html',context)

def show_account(request):
    user=request.user.customer_profile
    adress=Adress.objects.filter(owner=user,type='shipping')
    print(adress)
    badress=Adress.objects.filter(owner=user,type='biling')
    order_object=Order.objects.filter(customer=user).exclude(status=Order.cartstage).order_by('id')
    context={
        'adress':adress,
        'badress':badress,
        'orders':order_object,
         'user':user
            }
    return render(request,'account.html',context)

def show_order_details(request,order_number):
    order_object=Order.objects.get(order_number=order_number)
    print(order_object.order_items.all())
    user=request.user.customer_profile
    payment_obj = payment.objects.get(
                user=user,
                order=order_object,
    )
    shiping_obj=Shipping.objects.get(
                user=user,
                order=order_object,
            )
    if not order_object:
        messages.error(request,'order not found')
        return redirect('account')
    context={
        'orders':order_object,
        'shipping':shiping_obj,
        'payment':payment_obj
    }
    return render(request,'orderproces.html',context)

def edit_profile(request):
    if request.POST and ('update-form') in request.POST:
        print(request.POST)
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        customer=request.user.customer_profile
        if request.POST.get('email'):
            customer.email=email
        if request.POST.get('first_name'):
            customer.first_name=first_name
        if request.POST.get('last_name'):
            customer.last_name=last_name
        if request.POST.get('phone'):
            customer.phone=phone
        customer.save()
        return redirect('account')

def add_adress(request):
    if request.POST and ('adress') in request.POST:
        user=request.user.customer_profile
        adress_type=request.POST.get('type')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        street=request.POST.get('street')
        city=request.POST.get('city')
        landmark=request.POST.get('landmark')
        house_no=request.POST.get('house_no')
        state=request.POST.get('state')
        road_name=request.POST.get('road_name')
        name=request.POST.get('name')
        adresobj=Adress.objects.create(
            name=name,
            phonenumber=phone,
            type=adress_type,
            pincode=pincode,
            state=state,
            house_no=house_no,
            road_name=road_name,
            landmark=landmark,
            city=city,
            owner=user
        )
        adresobj.save()
        return redirect('account')

def delete_adress(request):
    if request.POST and ('delete') in request.POST:
        id=request.POST.get('id')
        obj=Adress.objects.get(pk=id)
        obj.delete()
    return redirect('account')


def show_about(request):
    return render(request,'about.html')

def register_page(request):
    if request.POST and ('signup-form') in request.POST:
        print(request.POST)
        if request.POST.get('username'):
            username = request.POST.get('username')
        else:
            username = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        try:
           
            if  User.objects.filter(username=username).exists():
                error_message='username already exists'
                messages.error(request,error_message) 
            user=User.objects.create_user(
            username=username,
            password=password
            )
            Customer.objects.create(
                first_name=first_name,last_name=last_name,
                email=email,phone=phone,user=user,
                )
            succes_message='account created succefully'
            login(request,user)
            messages.success(request,succes_message)
            return redirect('show_page')
        except Exception as e:
            error_message=e
            messages.error(request,error_message)
            print("note good")

    if request.POST and ('login-form') in request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(request.POST)
        try:
            user = authenticate(username=email,password=password)
            login(request,user)
            if ('remember-me') not in request.POST:
                request.session.set_expiry(0)
                print('not remember')
            return redirect('show_page')
        except Exception as e:
            error_message=e
            print(e,'hhhhhhhhhhhhhhhh')
            messages.error(request,error_message)
    return render(request,'register.html')

def user_logout(request):
    print('logouted')
    logout(request)
    request.session.flush()
    return redirect('show_page')


def change_password(request):
    if request.POST and ('change_password') in request.POST:
        new_password=request.POST.get('new_password')
        confirm_password=request.POST.get('confirm_password')
        if new_password == confirm_password:
            user=request.user
            user.set_password(new_password)
            user.save()
        else:
            messages.error(request,'enter password correctly')
        return redirect('account')
