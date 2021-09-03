from django.db import models
from ..file.models import Attachment


# 咖啡分类


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

# 咖啡


class Coffe(models.Model):
    coffe_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    vote = models.IntegerField()
    category = models.ForeignKey(Category, on_delete == models.CASCADE)
    picture = models.ForeignKey(Attachment)
