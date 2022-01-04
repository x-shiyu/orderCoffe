from django.db import models
from UserInfo.models import Shop, User,Promotion
from apps.Goods.models import Goods




class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Goods)
    # 实际付款
    real_pay = models.FloatField(default=0)
    status = models.IntegerField()
    # 使用积分付款
    abstract_pay = models.FloatField(default=0) 
    # 当前订单使用的折扣id
    promotion = models.ForeignKey(Promotion,on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)
