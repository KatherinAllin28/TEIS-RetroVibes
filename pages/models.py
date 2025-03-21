from django.db import models

class Vinyl(models.Model):
    name = models.CharField(max_length=255)
    imageDesign = models.ImageField(upload_to='templates/image')
    size = models.FloatField()
    colour = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=19.99)


