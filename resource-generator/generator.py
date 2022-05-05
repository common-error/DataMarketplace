import json,random,ciso8601 as cs,datetime,isodate

from numpy import outer

DEFAULTPATH = "./pool.json"

class randomize():

    def __init__(self,_path = DEFAULTPATH):
        self.data = json.load(open(_path))


    
    def generate(self,_start,_end):
        output = {
            "data" : []
        }

        for x in range(_start,_end):
            output["data"].append({
                "id":str(x),
                "data":str(bytes("risorsa "+str(x),"utf-8")),
                "metadata": self.randomMetadata()
            })
        
        with open('resources.json', 'w') as f:
            json.dump(output, f)

    def bpm(self):
        bpm = self.data["corsa"]["bpm"]
        gen_lvl = random.randint(0,bpm["GDD"]-1)

        if(gen_lvl == 0):
            return None
        else:
            return random.randint(bpm["start"],bpm["end"])
        
        
    
    def date(self):
        d = self.data["corsa"]["date"]
        start = cs.parse_datetime(d["start"])
        end = cs.parse_datetime(d["end"])
        gen_lvl = random.randint(0,d["GDD"]-1)

        days_between_dates = (end-start).days
        random_days = random.randrange(days_between_dates)
        
        if(gen_lvl == 0):
            return None
        elif(gen_lvl == 1):
            return "{}".format((start + datetime.timedelta(days=random_days)).year)
        elif(gen_lvl == 2):
            format = '%Y-%m'
            return "{}".format((start + datetime.timedelta(days=random_days)).strftime(format))
        else:
            return "{}".format((start + datetime.timedelta(days=random_days)).date())
 

    def step(self):
        step = self.data["corsa"]["step"]
        gen_lvl = random.randint(0,step["GDD"]-1)

        if(gen_lvl == 0):
            return None
        else:
            return random.randint(step["start"],step["end"])

    def sex(self):
        sex = self.data["corsa"]["sex"]
        gen_lvl = random.randint(0,sex["GDD"]-1)

        if(gen_lvl == 0):
            return None
        else:
            return sex["value"][random.randint(0,1)]

    def duration(self):
        duration = self.data["corsa"]["duration"]
        start = isodate.parse_duration(duration["start"])
        end = isodate.parse_duration(duration["end"])

        minutes_between_time = int((end-start).total_seconds() /60)
        random_min = random.randrange(minutes_between_time)


        return "{}".format(isodate.duration_isoformat((start + datetime.timedelta(minutes=random_min))))
   

    options = {
        "bpm":bpm,
        "date":date,
        "step":step,
        "sex":sex,
        "duration":duration
    }


    def randomMetadata(self):
        metadata = {}
        keys = list(self.data["corsa"].keys())
        random_idx = self._randomIxd(len(keys)-2)
        random_idx.extend([3,4])

        for idx in random_idx:
            metadata[keys[idx]] = self.options[keys[idx]](self)

        return metadata

    def _randomIxd(self, _len):
        return random.sample(range(_len),random.randint(0,_len))

        

r = randomize().generate(0,100)
