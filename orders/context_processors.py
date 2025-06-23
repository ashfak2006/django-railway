from .models import Order_item,Order

def cartitem_count(request):
    cart_obj={}
    if request.user.is_authenticated:
        try:
            user=request.user.customer_profile
            cart_obj=Order.objects.get(
                customer=user,
                status=Order.cartstage
            )
        except Exception as e:
            print(e)
    return {'cart':cart_obj}
