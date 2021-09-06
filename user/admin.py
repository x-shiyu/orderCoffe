from django.contrib import admin
from user.models import User, Group, Business

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Business)
