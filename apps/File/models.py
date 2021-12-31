from django.db import models

"""
# 附件
"""


class Attachment(models.Model):
    file_name = models.CharField(max_length=200)
    ext = models.CharField(max_length=20)
    file_path = models.TextField()
    file_size = models.FloatField(default=0)
