import json
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