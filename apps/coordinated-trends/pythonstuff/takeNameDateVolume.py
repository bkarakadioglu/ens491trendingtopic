import json

filename = "Turkey_2022-07.json"

with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        resultAsof = dict()
        resultVolume = dict()
        #Get the objects with form {"as_of": 21, trends:[{name:a, tweet_volume:1},{name:a, tweet_volume:1}...]}
        for singleObject in data:
                #Get the trends object with form {name:a, tweet_volume:1}
                for trend in singleObject["trends"]:         
                        resultAsof.setdefault(trend["name"], []).append(singleObject["as_of"])
                        resultVolume.setdefault(trend["name"], []).append(trend["tweet_volume"])
        arrRequired = []
        for name in resultVolume:
            arrRequired.append({ 'name' : name, 'asOf' : resultAsof[name], 'volumes' : resultVolume[name]})
        json.dump(arrRequired, open('newdat2a.json','w'))
