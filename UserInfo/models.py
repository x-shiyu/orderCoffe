from django.db import models
from File.models import Attachment
from Goods.models import Promotion
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class Group(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(default=1)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.password = password;
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
    thumb = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(default=18)
    # 积分
    abstract_money = models.FloatField(default=0)
    sex = models.CharField(max_length=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    objects = UserManager()

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
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    monthSell = models.IntegerField(default=0)

