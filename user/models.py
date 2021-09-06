from django.db import models
from django.db import models
from file.models import Attachment
from goods.models import Promotion


class GroupEnum(models.IntegerChoices):
    CONSUMER = 1
    BUSINESS = 2


class Group(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(default=1, choices=GroupEnum.choices)


class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=20)
    picture = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(default=18)
    money = models.FloatField(default=0)
    sex = models.CharField(max_length=2)
    abstract_money = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Business(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200)
    picture = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
