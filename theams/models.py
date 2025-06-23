from django.db import models

# Create your models here.
class Home_Banner(models.Model):
    image = models.ImageField(upload_to='theams/home_banner/')
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    content = models.TextField(null=True, blank=True)

