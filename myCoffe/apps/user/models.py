from django.contrib.auth.models import User as AuthUser
from django.db import models

from ..file.models import Attachment
# 用户


class User(AuthUser):
    picture = models.ForeignKey(Attachment)
    phone = models.CharField(max_length=11)
