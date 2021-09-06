from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from user.models import User, Group, Business, GroupEnum
import json


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        formData = json.loads(request.body.decode(encoding="utf-8"))
        try:
            sameUser = User.objects.get(username=formData['username'])
        except:
            group = Group.objects.get(code=GroupEnum.CONSUMER)
            user = User.objects.create(
                username=formData['username'], password=formData['password'], group=group)

        finally:
            return HttpResponse('post')
