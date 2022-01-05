import json
from os import X_OK
from django.shortcuts import render
from django.http import HttpResponse, FileResponse,HttpResponseBadRequest
from .models import Attachment
# Create your views here.
import re
import time


def getFile(request):
    fileId = request.GET['id']
    pattern = re.compile(r'^\d+$') 
    res = re.search(pattern, fileId, flags=0)
    if res != None:
      try:
        fileObj = Attachment.objects.get(id=fileId)
      except Attachment.DoesNotExist:
        fileObj = {"file_path":'static/default.png'}
      file = open(fileObj.file_path, 'rb')
      response = FileResponse(file)
      response['Content-Type'] = 'application/octet-stream'
      # response['Content-Disposition'] = 'attachment;filename="BatchPayTemplate.xls"'
      return response
    return HttpResponseBadRequest()

def upload(request):
    file_obj = request.FILES.get('file', None)
    response = HttpResponse()
    fileArr = file_obj.name.split('.')
    savePath = 'static/upload/' + str(int(time.time()))+'_'+file_obj.name
    with open(savePath, 'wb') as f:
        for line in file_obj.chunks():
            f.write(line)
    f.close()
    try:
        file = Attachment.objects.create(file_name=str(time.time(
        ))+'_'+file_obj.name, ext=fileArr[1], file_path=savePath, file_size=file_obj.size)
    except Exception as e:
        print(e)
        response.status_code = 500
        response.content = '上传文件失败'
        return response
    response.content = json.dumps({
        "msg": '上传成功',
        "fileId": file.id,
        "filePath":savePath
    })
    response.status_code = 200
    return response
