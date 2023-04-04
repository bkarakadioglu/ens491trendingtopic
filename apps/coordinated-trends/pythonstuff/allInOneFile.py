import fileinput
import os
import json
import time
from unidecode import unidecode

#Here is the order: turnJsonsToJson, removeCreatedAt, mergeJsonFiles, takeNameDateVolume, sortDateAndVolume, sessionCreator
filenames = ["Eskişehir_2023-01.jsons", "Eskişehir_2023-02.jsons", "Eskişehir_2023-03.jsons"]
allFile = "Eskişehir_All.json"
lowercasedFile = "Eskişehir_All_Lowercased.json"
timedFile = "Eskişehir_All_Timestamped.json"
sortedFile = "Eskişehir_Sorted.json"
finalFile = "Eskişehir.json"
interval = 10800000 #3 hours, if the times between the end and beginning of asofs are greater than 3 hours, a new session is created
                    #Otherwise the session continues

#Have the extracted jsons file in the directory
#Play with the variables above without changing the variable name
#No need to change below this line

def merge_JsonFiles(filenames):
    result = list()
    for filename in filenames:
        with open(filename, 'r') as infile:
            result.extend(json.load(infile))

    with open(allFile, 'w') as output_file:
        json.dump(result, output_file)

#Change from jsons format to json format
for filename in filenames:
    for line in fileinput.input(filename, inplace=True):
        if 1 != fileinput.filelineno():
            print(',{}'.format(line), end='')
        else:
            print('[{}'.format(line), end='')
    open(filename,"a").write(']')

#Change from .jsons extenstion to .json
for filename in filenames:
    os.rename(filename, filename[:-1])
    filenames[filenames.index(filename)] =  filename[:-1]

#Remove created at
for filename in filenames:
    with open(filename, "r+") as jsonFile:
        data = json.load(jsonFile)
        for element in data:
            del element["created_at"]
        jsonFile.seek(0)
        json.dump(data, jsonFile)
        jsonFile.truncate()
#Merges all the json into one file named by allFile variable
merge_JsonFiles(filenames)


#Changes Turkish letters to english, lowercases and adds a hashtag 
with open(allFile, "r") as jsonFile:
        data = json.load(jsonFile)
        arrLowercase = []
        #Get the objects with form {"as_of": 21, trends:[{name:a, tweet_volume:1},{name:a, tweet_volume:1}...]}
        for singleObject in data:
                trendsAltered = []
                #Get the trends object with form {name:a, tweet_volume:1}
                for trend in singleObject["trends"]:
                        #Change Turkish letters to English 
                        newTrendName = unidecode(trend['name'])     
                        newTrendName = newTrendName.lower()
                        #If there is no hashtag add one
                        if newTrendName[0] != '#':
                                newTrendName = "#" + newTrendName
                        trendsAltered.append({'name': newTrendName , "tweet_volume": trend["tweet_volume"]})
                arrLowercase.append({"as_of": singleObject["as_of"], "trends": trendsAltered})
        json.dump(arrLowercase, open(lowercasedFile,'w'))

#Changes json from {asof: trends:[{name:, tweet_volume:}...]} format to {name: asof:[] volumes:[]} format then puts it to a file name timedFile
with open(lowercasedFile, "r") as jsonFile:
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
        json.dump(arrRequired, open(timedFile,'w'))


#Sorts asofs then puts it into sortedFile
newArrRequired = []
with open(timedFile, "r") as jsonFile:
        data = json.load(jsonFile)
        #Get the objects with form {"name": name, "asOf": [date1,date2...], volumes:[123321,123123...]}
        for singleObject in data:
                asOfList = singleObject["asOf"]
                volumesList = singleObject["volumes"]
                #Zipping it to sort asOf and volumes together by asOf
                zipped = zip(asOfList, volumesList)
                zippedSorted = sorted(zipped,  key=lambda x: x[0]) 
                #Creating the object again in a sorted fashion
                asOfListSorted = []
                volumesListSorted = []
                for i in range(len(asOfList)):
                        asOfListSorted.append(zippedSorted[i][0])
                        volumesListSorted.append(zippedSorted[i][1])      
                newArrRequired.append({ 'name' : singleObject["name"], 'asOf' : asOfListSorted, 'volumes' : volumesListSorted})
        print(len(data))
        json.dump(newArrRequired, open(sortedFile,'w'))

finalArrRequired = []
with open(sortedFile, "r") as jsonFile:
        data = json.load(jsonFile)
        #Get the objects with form {"name": name, "asOf": [date1,date2...], volumes:[123321,123123...]}
        for singleObject in data:
            sessions = []
            sessionLengths = []
            sessionMaxVolume = []
            asOfList = singleObject["asOf"]
            volumesList = singleObject["volumes"]
            for i in range(len(asOfList)):
                    #If this is the first asof
                    if i == 0:
                            sessions.append([asOfList[i],asOfList[i]])
                            sessionLengths.append(1)
                            sessionMaxVolume.append(volumesList[i])
                            #If there is only one asof
                            if  len(asOfList) == 1:
                                break
                            #If there are more asofs
                            else:
                                    #If the second asof still belongs to the first session,
                                    #If there only 2 asofs it also means there are exactly one session with length two
                                    if asOfList[1] - asOfList[0] < interval:
                                            #Increase ses length and edit the last sessions end time
                                            sessions[0][1] = asOfList[1]
                                            sessionLengths[0] += asOfList[1] - asOfList[0]  
                                            #If the second volume is higher than the first one
                                            if volumesList[1] is not None and volumesList[0] is not None and volumesList[1] > volumesList[0]:
                                                    sessionMaxVolume[0] = volumesList[1]
                                    #Else it should create the second session with length one,
                                    #If there only 2 asofs also means there are exactly two sessions each of them with one length
                                    else:
                                            sessions.append([asOfList[1],asOfList[1]])
                                            sessionLengths.append(1)
                                            sessionMaxVolume.append(volumesList[1])
                                    if len(asOfList) == 2:       
                                        break    
                    #If this is the last asof
                    elif i == len(asOfList) - 1:
                        break             
                    #If the next asof is within 20 minutes
                    elif asOfList[i+1] - asOfList[i] < interval:
                                #Increase ses length and edit the last sessions end time
                                sessions[len(sessions)-1][1] = asOfList[i+1]
                                sessionLengths[len(sessionLengths)-1] += asOfList[i+1] - asOfList[i]
                                #If the next volume is higher than the biggest one
                                if volumesList[i+1] is not None and sessionMaxVolume[len(sessions)-1] is not None and volumesList[i+1] > sessionMaxVolume[len(sessions)-1]:
                                        sessionMaxVolume[len(sessions)-1] = volumesList[i+1]
                    #Else it means there is a new session
                    else:
                            sessions.append([asOfList[i+1],asOfList[i+1]])
                            sessionLengths.append(1)
                            sessionMaxVolume.append(volumesList[i+1])

            sessionStarts = []
            sessionEnds = []
            sessionLengthsInHours = []
            #Change lengths to hours
            for i in sessionLengths:
                       sessionLengthsInHours.append(i/3600000)
            for i in sessions:
                    sessionStarts.append(i[0])     
                    sessionEnds.append(i[1]) 

            """ sessionLengthsInHours2 = []
            for i in range(len(sessionEnds)):
                    sessionLengthsInHours2.append((sessionEnds[i] - sessionStarts[i])/3600000) """
                    
            finalArrRequired.append({ 'name' : singleObject["name"], 'sessionStart' : sessionStarts,
                                'sessionEnd':sessionEnds, 'sesLength' : sessionLengthsInHours,
                                'sessionMaxVolume': sessionMaxVolume})

        json.dump(finalArrRequired, open(finalFile,'w'))
