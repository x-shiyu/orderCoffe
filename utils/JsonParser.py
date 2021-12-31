import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
class JsonParser():
    def __init__(self,json_str) -> None:
        self.json_data = json.loads(json_str)
    def getValue(self,key):    
        return self.json_data[key]
    def getValues(self,keys):
        keys_dict = {}
        for key in keys:
            if self.json_data[key]:
                keys_dict[key] = self.json_data[key]
        return keys_dict

def formatJson(querySet):
  temp_output = serializers.serialize('python', querySet,ensure_ascii=False)
  output = json.dumps(temp_output, cls=DjangoJSONEncoder)
  return output