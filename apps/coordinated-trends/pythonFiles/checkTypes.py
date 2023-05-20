import json
filename = "Turkey_All_Timestamped.json"
arrRequired = dict()
with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        #Get the objects with form {"name": name, "asOf": [date1,date2...], volumes:[123321,123123...]}
        for singleObject in data:
                name = singleObject["name"]
                asOfList = singleObject["asOf"]
                volumesList = singleObject["volumes"]
                if type(singleObject["name"]) in arrRequired:
                        arrRequired[type(singleObject["name"])] += 1
                else:
                        arrRequired[type(singleObject["name"])] = 1

                for i in asOfList:
                       a = str(type(i)) + "asof" 
                       if a in arrRequired:
                        arrRequired[a] += 1
                       else:
                        arrRequired[a] = 1 
                
                for i in volumesList:
                       a = str(type(i)) + "vol" 
                       if a in arrRequired:
                        arrRequired[a] += 1
                       else:
                        arrRequired[a] = 1 

        print(arrRequired)