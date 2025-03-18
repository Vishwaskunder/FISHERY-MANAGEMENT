from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
class User(AbstractUser):
    is_user = models.BooleanField('is_user', default=False)
    is_admin = models.BooleanField('is_admin', default=False)
    phone_number = models.CharField('Phone Number', max_length=15, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser and not self.is_admin:
            self.is_admin = True
        super().save(*args, **kwargs)

class FishDetails(models.Model):
    fish_id = models.AutoField(primary_key=True)
    fish_name = models.CharField('Fish Name', max_length=100)
    fish_price = models.DecimalField('Fish Price', max_digits=10, decimal_places=2)
    fish_quantity = models.PositiveIntegerField('Fish Quantity')
    date = models.DateField('Date', auto_now_add=True)



class Orders(models.Model):
    ordered_by=models.ForeignKey(User,on_delete=models.CASCADE)
    fish=models.ForeignKey(FishDetails,on_delete=models.CASCADE,blank=True)
    quantity=models.IntegerField('Quantity')
    total=models.DecimalField("total",max_digits=10, decimal_places=2)
    date = models.DateField('Date', auto_now_add=True, null=True)
    