from django.db import models
from users.models import Customer,Adress
from products.models import products
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class Discount(models.Model):
    promo_code=models.CharField(max_length=15,unique=True)
    isvalid=models.BooleanField(default=False)
    max_users=models.IntegerField(null=True,blank=True)
    used_count=models.IntegerField(blank=True,null=True,default=0)
    valid_to=models.DateField()
    valid_from=models.DateField()
    fixed_amount=models.IntegerField(blank=True,null=True)
    percentage_rate=models.IntegerField(blank=True,null=True)
    TYPE=(
        ('PERCENTAGE','PERCENTAGE'),
        ('FIXED','FIXED')
    )
    discount_type=models.CharField(choices=TYPE,default='PERCENTAGE')

    
    def __str__(self):
        return self.promo_code
    
    def save(self, *args,**kwargs):
        if self.used_count >= self.max_users:
            self.isvalid = True
        else:
            self.isvalid = False
        super().save(*args,**kwargs)
    


class Order(models.Model):
    cartstage=0
    pending=1
    processing=2
    shipped=3
    deliverd=4
    cancelled=5
    refunded=6
    ORDER_STATUS=(
        (cartstage,'cartstage'),
        (pending,'pending'),
        (processing,'procesing'),
        (shipped,'shipped'),
        (deliverd,'deliverd'),
        (cancelled,'cancelled'),
        (refunded,'refunded')
    )
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orders')
    order_number=models.CharField(max_length=15,unique=True)
    promocode=models.ForeignKey(Discount,on_delete=models.SET_NULL,related_name='applied_orders',null=True,blank=True)
    order_date=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    total_amount=models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    grand_total=models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    status=models.IntegerField(choices=ORDER_STATUS,default=0)


    def __str__(self):
        return f"order #{self.order_number}-{self.customer}"
    
    def mark_as_shipped(self):
        self.status=3
        self.shipping.mark_as_shipped()
        self.save()
    def mark_as_deliverd(self):
        self.status=4
        self.shipping.mark_as_delivered()
        self.save()

    def mark_as_procesing(self):
        self.status=2
        self.processed_at = timezone.now()
        self.save()

    def set_total_amount(self):
        total = sum(item.total_price for item in self.order_items.all())
        self.total_amount = total
        self.save()

    def set_grand_total(self):
        self.grand_total =  self.total_amount + int(self.shipping.cost)
        self.save()

    def aplly_discount(self,disc):
        self.grand_total = self.total_amount - int(disc)
        self.save()
        

    def save(self, *args,**kwargs):
        if not self.order_number:
            last_order=Order.objects.order_by('-id').first()
            last_id = last_order.id if last_order else 0
            self.order_number =f"ORD-{last_id + 1:06d}"
        super().save(*args,**kwargs)

class payment(models.Model):
    STATUS=(
        ('pending','pending'),
        ('completed','completed'),
        ('failed','failed'),
        ('refunded','refunded'),
        ('canceled','canceled')
    )
    PAYMENT_METHOD_CHOICES = [
        ('debit_card', 'Debit Card'),
        ('upi', 'upi'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery','cash on delivery')
    ]
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='payments')
    order = models.ForeignKey(Order,on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2,)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    transaction_id = models.CharField(max_length=100, unique=True)
    gateway_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    gateway_response = models.JSONField(blank=True, null=True)

    billing_address = models.ForeignKey(Adress,on_delete=models.DO_NOTHING,related_name='payments',null=True,blank=True)

    error_message = models.TextField(blank=True, null=True)

    is_paid=models.BooleanField(default=False)
    tax_rate=models.DecimalField(decimal_places=2,max_digits=10,default=18)
    tax_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0,null=True,blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['status']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def _str_(self):
        return f"Payment {self.transaction_id} - {self.amount}"
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
    
    def generate_transaction_id(self):
        import uuid
        return f"txn_{uuid.uuid4().hex[:16]}"
    
    
    
    def mark_as_completed(self, gateway_response=None):
        self.status = 'completed'
        self.gateway_response = gateway_response
        self.processed_at = timezone.now()
        self.save()
    
    def mark_as_failed(self, error_message=None):
        self.status = 'failed'
        self.error_message = error_message
        self.processed_at = timezone.now()

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)
    
    def generate_transaction_id(self):
        import uuid
        return f"txn_{uuid.uuid4().hex[:16]}"

class Order_item(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product=models.ForeignKey(products,on_delete=models.PROTECT)
    quantity=models.IntegerField(default=1)
    unit_price=models.DecimalField(decimal_places=2,max_digits=10,default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    total_price=models.DecimalField(decimal_places=2,max_digits=10,default=0,null=True,blank=True)
    def __str__(self):
        return f"{self.quantity}*{self.product.title} (order #{self.order.order_number})"
    @property
    def total_count(self):
        return self.order.items.count()
    def save(self, *args,**kwargs):
        self.total_price=self.quantity * self.unit_price
        super().save(*args,**kwargs)

class Shipping(models.Model):
    SHIPPING_METHOD_CHOICES = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
        ('overnight', 'Overnight Shipping'),
        ('international', 'International Shipping'),
        ('pickup', 'Store Pickup'),
    ]

    SHIPPING_STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('ready_for_shipment', 'Ready for Shipment'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('failed', 'Delivery Failed'),
    ]
    
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='shipping')
    user = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='shippings')
    shipping_method = models.CharField(max_length=20,choices=SHIPPING_METHOD_CHOICES,default='standard')
    tracking_number = models.CharField(max_length=50,blank=True,null=True,unique=True)
    carrier = models.CharField(max_length=50,blank=True,null=True)  # e.g., FedEx, UPS, USPS
    status = models.CharField(max_length=20,choices=SHIPPING_STATUS_CHOICES,default='processing')

    cost = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    is_free = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(Adress,on_delete=models.SET_NULL,related_name='shipments',blank=True, null=True)

    Notes=models.TextField(blank=True,null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Shipping'
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Shipping #{self.id} for Order {self.order.id}"

    def change_cost(self):
        base_cost=70
        if self.order.total_amount > 1000:
            self.cost=0
            self.is_free = True 
        else:
            if self.shipping_method=='express':
                self.cost=base_cost+100
            elif self.shipping_method=='overnight':
                self.cost=base_cost+200
            elif self.shipping_method=='international':
                self.cost=base_cost+500
            elif self.shipping_method=='pickup':
                self.cost=base_cost+100
            else:
                self.cost = 70
        self.save()   

    def save(self, *args, **kwargs):
        if not self.tracking_number and self.status in ['shipped', 'in_transit']:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)

    def generate_tracking_number(self):
        import uuid
        return f"TRK{uuid.uuid4().hex[:12].upper()}"

    def mark_as_shipped(self):
        self.status = 'shipped'
        self.order.mark_as_shipped()
        self.shipped_at = timezone.now()
        self.save()

    
    def mark_as_delivered(self):
        self.status = 'delivered'
        self.order.mark_as_shipped()
        self.delivered_at = timezone.now()
        self.save()

    def calculate_estimated_delivery_date(self):
        """Calculate estimated delivery date based on shipping method"""
        order_time=self.order.processed_at
        if self.shipping_method == 'overnight':
            return order_time + timedelta(days=1)
        elif self.shipping_method == 'express':
            return order_time + timedelta(days=4)
        elif self.shipping_method == 'pickup':
            return order_time + timedelta(days=3)
        elif self.shipping_method == 'international':
            return order_time + timedelta(days=12)
        else:  # standard
            return order_time + timedelta(days=7)
        

