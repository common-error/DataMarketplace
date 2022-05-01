import json,random,ciso8601 as cs,datetime,isodate

from numpy import outer

DEFAULTPATH = "./pool.json"

class randomize():

    def __init__(self,_path = DEFAULTPATH):
        self.data = json.load(open(_path))


    
    def generate(self,_quantity):
        output = {
            "data" : []
        }

        for x in range(_quantity):
            output["data"].append({
                "id":str(x),
                "data":str(bytes("risorsa "+str(x),"utf-8")),
                "metadata": self.randomMetadata()
            })
        
        with open('resources.json', 'w') as f:
            json.dump(output, f)

    def bpm(self):
        bpm = self.data["corsa"]["bpm"]
        return random.randint(bpm["start"],bpm["end"])
    
    def date(self):
        d = self.data["corsa"]["data"]
        start = cs.parse_datetime(d["start"])
        end = cs.parse_datetime(d["end"])

        days_between_dates = (end-start).days
        random_days = random.randrange(days_between_dates)

        return "{}".format((start + datetime.timedelta(days=random_days)).date())


    def step(self):
        step = self.data["corsa"]["step"]
        return random.randint(step["start"],step["end"])

    def sex(self):
        sex = self.data["corsa"]["sex"]
        return sex[random.randint(0,1)]

    def duration(self):
        duration = self.data["corsa"]["duration"]
        start = isodate.parse_duration(duration["start"])
        end = isodate.parse_duration(duration["end"])

        minutes_between_time = int((end-start).total_seconds() /60)
        random_min = random.randrange(minutes_between_time)
        
        return "{}".format(isodate.duration_isoformat((start + datetime.timedelta(minutes=random_min))))

    options = {
        "bpm":bpm,
        "data":date,
        "step":step,
        "sex":sex,
        "duration":duration
    }


    def randomMetadata(self):
        metadata = {}
        keys = list(self.data["corsa"].keys())
        random_idx = random.sample(range(len(keys)),random.randint(0,len(keys)))

        for idx in random_idx:
            metadata[keys[idx]] = self.options[keys[idx]](self) if bool(random.getrandbits(1)) else None

        return metadata



        

r = randomize().generate(30)
