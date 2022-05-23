import json,os,requests
from os.path import exists
from pickle import FALSE

DEFAULTPATH = "D:\\Users\\richi\\Desktop\\DataMarketplace\\mapping.json"

class map():

    def __init__(self, _mappingName = DEFAULTPATH,_bytes=3):
        #print(os.getcwd())
        self.bytes = _bytes
        if(exists(_mappingName)):
            self.M = self._readFile(_mappingName)
        else:
            print("Mapping not founf!\nCreating one from scratch")
            self.M = {}

    def add(self,_value):
        if(_value != ""):
            if(_value  in self.M):
                return self.M[_value]
            rndMap = ""
            while(True):
                rndMap = os.urandom(self.bytes)
                if(rndMap not in self.M.values()):
                    break

            self.M[_value] = rndMap.hex()

            return self.M.get(_value)

    def get(self,_value):
        
        return self.M.get(_value)
        
        

    def save(self, _mappingName = DEFAULTPATH,_pubKey = "",_baseUrl=""):
        with open(_mappingName, 'w') as f:
            json.dump(self.M, f)
        
        if _pubKey != "":
            data_to_send = {
                "map":json.dumps(self.M)
            }

            url = "{}mapping/{}".format(_baseUrl,_pubKey)

            response = requests.post(url,data_to_send)



    def _readFile(self,_path):
        try:
            with open(_path, 'r') as f:
                return json.load(f)
        except Exception as ex:
            print(ex)      
        