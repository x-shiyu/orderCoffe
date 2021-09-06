from django.db import models
from file.models import Attachment


# 咖啡分类
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)


class FullReduce(models.Model):
    f_price = models.FloatField()
    t_price = models.FloatField()


class PromotionWay(models.IntegerChoices):
    DISCOUNT = 1  # 打折
    FULLREDUCE = 2  # 满减
    NULL = 0  # 没有促销


class Promotion(models.Model):

    # 促销方式
    promotion_way = models.IntegerField(
        choices=PromotionWay.choices, default=PromotionWay.NULL)
    # 折扣
    discount_per = models.FloatField()
    # 满减
    full_reduce_range = models.ManyToManyField(FullReduce)


class Coffe(models.Model):
    coffe_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    # 投票数
    vote = models.IntegerField(default=0)
    # 折扣
    discount = models.FloatField()
    # 促销
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    # 积分
    abstract_money = models.IntegerField(default=0)
    pay_with_abstract_money = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ForeignKey(Attachment, on_delete=models.CASCADE)
