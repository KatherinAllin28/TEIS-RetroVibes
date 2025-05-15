from django.db import models
from django.contrib.auth.models import User

class Vinyl(models.Model):
    name = models.CharField(max_length=255)
    imageDesign = models.ImageField(upload_to='templates/image')
    size = models.FloatField()
    colour = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=19.99)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vinyls = models.ManyToManyField(Vinyl, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped')], default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=[('in_transit', 'In Transit'), ('delivered', 'Delivered')], default='in_transit')
    estimated_delivery = models.DateField()
