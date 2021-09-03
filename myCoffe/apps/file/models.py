from django.contrib.auth import models

"""
# 附件
"""


class Attachment(models.Model):
    file_name = models.CharField(max_length=200)
    ext = models.CharField(max_length=20)
    path = models.CharField()
