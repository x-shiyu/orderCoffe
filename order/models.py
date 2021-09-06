from django.db import models
from user.models import Business, User
from goods.models import Coffe
# Create your models here.


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Coffe)
    price = models.FloatField(default=0)
