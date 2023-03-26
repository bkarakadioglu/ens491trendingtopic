import json
filename = "TurkeyAllReadySorted.json"
arrRequired = []
interval = 3600000 #1 hour
with open(filename, "r") as jsonFile:
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
                                            sessionLengths[0] += 1  
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
                                sessionLengths[len(sessionLengths)-1] += 1
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
            for i in sessions:
                    sessionStarts.append(i[0])     
                    sessionEnds.append(i[1]) 
            arrRequired.append({ 'name' : singleObject["name"], 'sessionStart' : sessionStarts,
                                'sessionEnd':sessionEnds, 'sesLength' : sessionLengths,
                                'sessionMaxVolume': sessionMaxVolume, 'sesCount':len(sessionMaxVolume)})

        json.dump(arrRequired, open('template7.json','w'))
