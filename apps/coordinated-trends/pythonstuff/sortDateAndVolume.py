import json
filename = "Eskisehir_All_Timestamped.json"
arrRequired = []
with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        #Get the objects with form {"name": name, "asOf": [date1,date2...], volumes:[123321,123123...]}
        for singleObject in data:
                asOfList = singleObject["asOf"]
                volumesList = singleObject["volumes"]
                #Zipping it to sort asOf and volumes together by asOf
                zipped = zip(asOfList, volumesList)
                zippedSorted = sorted(zipped) 
                #Creating the object again in a sorted fashion
                asOfListSorted = []
                volumesListSorted = []
                for i in range(len(asOfList)):
                        asOfListSorted.append(zippedSorted[i][0])
                        volumesListSorted.append(zippedSorted[i][1])      
                arrRequired.append({ 'name' : singleObject["name"], 'asOf' : asOfListSorted, 'volumes' : volumesListSorted})
        print(len(data))
        json.dump(arrRequired, open('EskisehirSorted.json','w'))