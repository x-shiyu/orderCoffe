from django.db import models
from apps.File.models import Attachment
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Group(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(default=1)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
        )
        return user

    def create_superuser(self, email, firstname, lastname, phone, password=None):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    thumb = models.ForeignKey(Attachment, on_delete=models.CASCADE,blank=True,null=True)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(default=18)
    # 积分
    abstract_money = models.FloatField(default=0)
    sex = models.CharField(max_length=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email + ", " + self.nickname


# 商铺
class Shop(models.Model):
    name = models.CharField(max_length=100)
    # 所属用户
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200)
    thumb = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    monthSell = models.IntegerField(default=0)
    autoAccept = models.BooleanField(default=True)


class Promotion(models.Model):
    full = models.FloatField()
    min = models.FloatField()
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE)
