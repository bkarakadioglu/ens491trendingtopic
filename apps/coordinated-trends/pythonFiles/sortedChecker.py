import json
filename = "EskisehirSorted.json"
arrRequired = []
with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        #Get the objects with form {"name": name, "asOf": [date1,date2...], volumes:[123321,123123...]}
        boolArr = []
        for singleObject in data:
                boolArr.append(all(singleObject["asOf"][i] <= singleObject["asOf"][i+1] for i in range(len(singleObject["asOf"]) - 1)))
        print(all(boolArr))
        print(boolArr)
