from django.db import models
from users.models import Customer
from django.db.models import Avg,Count,F

# Create your models here.

class Catogaries(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(null=True,blank=True)
    slug=models.SlugField(max_length=200,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to=('media/catogary_images'),null=True,blank=True)
    banner=models.ImageField(upload_to=('media/catogary_images'),null=True,blank=True)

    class Meta:
        db_table_comment = "Catogaries"
        ordering = ["-created_at"]
        # verbose_name = "Catogary"
        # verbose_name_plural = "Catogaries"

    def __str__(self):
        return self.name


class products(models.Model):
    STOCK_CHOICES=[
        ('in_stock','in stock'),
        ('low_stock','low stock'),
        ('out_of_stock','out of stock')
    ]
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=200,unique=True)
    short_description=models.TextField(max_length=300,blank=True,null=True)
    description=models.TextField()
    sku=models.CharField(max_length=65,unique=True,blank=True,null=True)
    
    price=models.FloatField(max_length=12)
    sale_price=models.FloatField(max_length=12,blank=True,null=True)

    catogaris=models.ManyToManyField(Catogaries,related_name="products")

    stock=models.PositiveIntegerField()
    stock_status=models.CharField(choices=STOCK_CHOICES,default="in_stock")
    low_stock = models.PositiveIntegerField(default=4)

    weight=models.DecimalField(decimal_places=2,max_digits=6)
    purity=models.DecimalField(decimal_places=3,max_digits=6,default=18)

    isfetuerd=models.BooleanField()
    isbestseller=models.BooleanField()
    isnew=models.BooleanField()
    ishallmarked=models.BooleanField()

    image1=models.ImageField(upload_to=('media/product_images'))
    image2=models.ImageField(upload_to=('media/product_images'),blank=True,null=True)
    image3=models.ImageField(upload_to=('media/product_images'),blank=True,null=True)
    image4=models.ImageField(upload_to=('media/product_images'),blank=True,null=True)
    image5=models.ImageField(upload_to=('media/product_images'),blank=True,null=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table_comment = "products"
        ordering = ["-created_at"]
        verbose_name = "PRODUCT"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title
    @property
    def discount(self):
        return round(((self.price-self.sale_price)/self.price)*100)
    @property
    def review_count(self):
        return self.review.count()

    def save(self, *args, **kwargs):
        self.change_stock_status()
        super().save(*args, **kwargs)
    
    def change_stock_status(self):
        if self.stock <= 0:
            self.stock_status = 'out_of_stock'
        elif self.stock <= self.low_stock:
            self.stock_status = 'low_stock'

class Review(models.Model):
    RATING_CHOICES=[
        (1,'poor'),
        (2,'fair'),
        (3,'good'),
        (4,'verygood'),
        (5,'excelent')
    ]
    product=models.ForeignKey(products,on_delete=models.CASCADE,related_name="review")
    comment=models.TextField(max_length=250,null=True,blank=True)
    rating=models.PositiveSmallIntegerField(choices=RATING_CHOICES,default=1)
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="product_reviews")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=True)
    comment_title=models.TextField(max_length=50,null=True,blank=True)
    is_verifeid_purchaser=models.BooleanField(default=True)
    
    image1=models.ImageField(upload_to=('media/product_review'),blank=True,null=True)
    image2=models.ImageField(upload_to=('media/product_review'),blank=True,null=True)
    image3=models.ImageField(upload_to=('media/product_review'),blank=True,null=True)

    class Meta:
        db_table_comment = "REVIEWS"
        ordering = ["-created_at"]
        

    def __str__(self):
        return self.product.title
    
    @classmethod
    def get_average_rating(cls):
        return cls.objects.aggregate(average_rating=models.Avg('rating'))['average_rating']
    
    @property
    def total_count(self):
        return self.count()
    


  




    



