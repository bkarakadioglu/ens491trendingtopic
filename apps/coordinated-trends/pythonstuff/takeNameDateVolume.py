import json
import time
filename = "Eskisehir_All.json"

with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        resultAsof = dict()
        resultVolume = dict()
        #Get the objects with form {"as_of": 21, trends:[{name:a, tweet_volume:1},{name:a, tweet_volume:1}...]}
        for singleObject in data:
                #Get the trends object with form {name:a, tweet_volume:1}
                for trend in singleObject["trends"]:         
                        resultAsof.setdefault(trend["name"], []).append(int(time.mktime(time.strptime(singleObject["as_of"], '%Y-%m-%dT%H:%M:%SZ'))) * 1000)
                        resultVolume.setdefault(trend["name"], []).append(trend["tweet_volume"])
        arrRequired = []
        for name in resultVolume:
            arrRequired.append({ 'name' : name, 'asOf' : resultAsof[name], 'volumes' : resultVolume[name]})
        json.dump(arrRequired, open('Eskisehir_All_Timestamped.json','w'))
