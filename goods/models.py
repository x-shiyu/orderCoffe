from django.db import models
from File.models import Attachment


# 咖啡分类
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class Promotion(models.Model):
    full = models.FloatField()
    min = models.FloatField()


class Goods(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    # 投票数
    vote = models.IntegerField(default=0)
    # 折扣
    discount = models.FloatField()
    # 当前商品可用多少积分来抵扣
    abstract_money = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumb = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    # 月销售量
    month_sell = models.IntegerField(default=0)
