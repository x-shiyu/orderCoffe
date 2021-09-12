from django.db import models
from django.utils import tree
from file.models import Attachment
from goods.models import Promotion
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class GroupEnum(models.IntegerChoices):
    CONSUMER = 1
    BUSINESS = 2


class Group(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(default=1, choices=GroupEnum.choices)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        
        return user

    def isVip(self):
        return self.vip_level>0


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
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    picture = models.ForeignKey(Attachment, on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(default=18)
    money = models.FloatField(default=0)
    sex = models.CharField(max_length=2,default='男')
    abstract_money = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
    vip_level = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def is_vip(self):
        return self.vip_level>0
    
    def get_detail(self):
        return {
            "email":self.email,
            "username":self.username,
            "picture":self.picture,
            "phone":self.phone,
            "age":self.age,
            "money":self.money,
            "sex":self.sex,
            "abstract_money":self.abstract_money,
            "vip_level":self.vip_level,
        }
    def __str__(self):
        return self.email + ", " + self.username


class Business(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=200)
    picture = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
