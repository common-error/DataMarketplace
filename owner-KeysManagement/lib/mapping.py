import json,os
from os.path import exists

DEFAULTPATH = "../mapping.json"

class map():

    def __init__(self, _mappingName = DEFAULTPATH,_bytes=2):
        self.bytes = _bytes
        if(exists(_mappingName)):
            self.M = self._readFile(_mappingName)
        else:
            self.M = {}

    def add(self,_value):
        if(_value not in self.M):
            rndMap = ""
            while(True):
                rndMap = os.urandom(self.bytes)
                if(rndMap not in self.M.values()):
                    break

            self.M[_value] = rndMap.hex()

    def get(self,_value):
        return self.M[_value]
        

    def save(self, _mappingName = DEFAULTPATH):
        with open(_mappingName, 'w') as f:
            json.dump(self.M, f)


    def _readFile(self,_path):
        try:
            with open(_path, 'r') as f:
                return json.load(f)
        except Exception as ex:
            print(ex)      
        

m = map()
m.add("a")
m.add("b")
m.add("w")
m.add("ab")

print(m.get("ab"))
m.save()
