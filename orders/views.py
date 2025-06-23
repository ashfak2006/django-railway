from django.shortcuts import render,redirect
from .models import Order,Order_item,Discount,Shipping,payment
from products.models import products
from users.models import Adress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.models import Customer,Adress
# Create your views here.

@login_required(login_url='/register/')
def show_cart(request):
    user=request.user.customer_profile
    promocode=request.session.get('applied_coupen')
    DISCOUNT=0
    try:
        cart_obj=Order.objects.get(
            customer=user,
            status=Order.cartstage,
        )
        shiping_obj,created=Shipping.objects.get_or_create(
            user=user,
            order=cart_obj,
            cost=0
        )
        cart_obj.set_total_amount()
        if promocode:
            discout_obj=Discount.objects.get(promo_code=promocode,isvalid=True)
            if promocode and discout_obj.discount_type == 'PERCENTAGE':
                rate=discout_obj.percentage_rate
                DISCOUNT = rate * cart_obj.grand_total /100
                print('discount applied')
                request.session['discount_amount']=int(DISCOUNT)
            elif promocode and discout_obj.discount_type == 'FIXED':
                DISCOUNT = discout_obj.fixed_amount
                print('discount applied')
                request.session['discount_amount']=int(discout_obj.fixed_amount)
            cart_obj.promocode=discout_obj
            cart_obj.aplly_discount(DISCOUNT)
        shiping_obj.change_cost()
        cart_obj.set_grand_total()
        cart_obj.save()
        context={
            'cart':cart_obj,
            'DISCOUNT':DISCOUNT,
            'ship':cart_obj.shipping.cost
        }
        return render (request,'cart.html',context)
    except Exception as e:
        messages.error(request,e,'cart not found')
        return render (request,'cart.html')

@login_required(login_url='/register/')
def add_to_cart(request):
    if request.POST:
        user=request.user.customer_profile
        Quantity=int(request.POST.get('quantity'))
        Product_id=request.POST.get('product_id')
        Product=products.objects.get(pk=Product_id)
        order_obj,created=Order.objects.get_or_create(
            customer=user,
            status=Order.cartstage
        )
        order_item,created=Order_item.objects.get_or_create(
            order=order_obj,
            product=Product,
            unit_price=Product.sale_price
        )
        if Quantity >= Product.stock:
            Quantity = Product.stock
        Product.stock -= Quantity
        Product.save()
        if created:
            order_item.quantity=Quantity
            order_item.save()
        else:
            order_item.quantity=order_item.quantity + Quantity
            order_item.total_price=order_item.quantity * Product.sale_price
            order_item.save()
        
        previous_page = request.META.get('HTTP_REFERER')
        return redirect(previous_page)
    else:
        print('something wrong')
    return redirect('products_list')

def check_out(request):
    try:
        user=request.user.customer_profile
        adress=Adress.objects.get(
            owner=user,
            adress_type='Home',
            type='shipping'
        )
        cart_obj=Order.objects.get(
            customer=user,
            status=Order.cartstage,
        )
        shiping_obj=Shipping.objects.get(
            user=user,
            order=cart_obj,
        )
        cart_obj.save()
        shiping_obj.shipping_address = adress
        print(shiping_obj.shipping_address,shiping_obj.id)
        shiping_obj.change_cost()
        shiping_obj.save()
        context={
            'cart':cart_obj,
            'adress':shiping_obj.shipping_address
        }
        return render(request,'checkout.html',context)
    except Exception as e:
        print(e,'check out')
        return redirect('cart')


def remove_item_from_cart(request,pk):
    item=Order_item.objects.get(pk=pk)
    if item:
        item.product.stock += item.quantity
        item.product.save()
        item.delete()
    return redirect ('cart')

def apply_discount(request):
    if request.POST and ('Discount') in request.POST:
        try:
            promocode=request.POST.get('promocode')
            discout_obj=Discount.objects.get(promo_code=promocode,isvalid=True)
            discout_obj.used_count += 1
            discout_obj.save()
            if 'applied_coupen' in request.session:
                messages.error(request,' ALL READY A COUPON APPLIED')
            else:
                request.session['applied_coupen']=discout_obj.promo_code
                messages.success(request,'A COUPON APPLIED SUCCESFULLY')
        except:
            messages.error(request,'INVALID COUPEN CODE')
        return redirect('cart')
    
def remove_discount(request):
    if 'applied_coupen' in request.session:
        promocode = request.session['applied_coupen']
        discout_obj=Discount.objects.get(promo_code=promocode)
        discout_obj.used_count -= 1
        discout_obj.save()
        del request.session['applied_coupen']
        del request.session['discount_amount']
        user=request.user.customer_profile
        cart_obj,created=Order.objects.get_or_create(
            customer=user,
            status=Order.cartstage,      
        )
        cart_obj.promocode=None
        cart_obj.save()
        messages.success(request,' COUPON removed SUCCESFULLY')
    else:
        print('no way ')
    return redirect('cart')



def palce_order(request):
    user=request.user.customer_profile
    if request.POST and ('check_out') in request.POST:
        print(request.POST,'checkout')
        shippingMethod = request.POST.get('shippingMethod')
        payment_methode = request.POST.get('PaymnetMethod')
        note = 'some random notes'
        user=request.user.customer_profile
        try:
            cart_obj=Order.objects.get(
                customer=user,
                status=Order.cartstage
            )

            #check if order object exist if true redirect cart
            cart_obj.mark_as_procesing()

            payment_obj,created=payment.objects.get_or_create(
                user=user,
                order=cart_obj,
                payment_method=payment_methode,
                billing_address=cart_obj.shipping.shipping_address,
                amount=cart_obj.grand_total
            )
            print(payment_obj.status)
            print(payment_obj.payment_method)
            shiping_obj=Shipping.objects.get(
            user=user,
            order=cart_obj,
            )
            shiping_obj.shipping_method = shippingMethod
            shiping_obj.Notes = note
            shiping_obj.change_cost()
            cart_obj.set_grand_total()
            shiping_obj.save()
            context = {
                'orders':cart_obj,
                'shipping':shiping_obj,
                'payment':payment_obj
            }
            return render(request,'orderproces.html',context)
        except Order.DoesNotExist:
           messages.error(request,'there is something wronge in processing')
           return redirect('cart')
    return redirect('cart')

def cancel_order(request,order_number):
    order_obj=Order.objects.get(order_number=order_number)
    order_obj.status=5
    order_obj.save()
    context = {
        'orders':order_obj,
        'shipping':order_obj.shipping,
        'payment':order_obj.payments
    }
    return render(request,'orderproces.html',context)