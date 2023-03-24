import json

filename = "Turkey_2022-07.json"

with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        resultName = []
        resultAsof = []
        resultVolume = []
        #Get the objects with form {"as_of": 21, trends:[{name:a, tweet_volume:1},{name:a, tweet_volume:1}...]}
        for singleObject in data:
                #Get the trends object with form {name:a, tweet_volume:1}
                for trend in singleObject["trends"]:
                        resultName.append(trend["name"])         
                        resultAsof.append(singleObject["as_of"])
                        resultVolume.append(trend["tweet_volume"])
        arrRequired = []
        print(len(resultName),len(resultVolume),len(resultAsof))
        for i in range(len(resultVolume)):
            arrRequired.append({ 'name' : resultName[i], 'asOf' : resultAsof[i], 'volumes' : resultVolume[i]})
        json.dump(arrRequired, open('newdat32a.json','w'))