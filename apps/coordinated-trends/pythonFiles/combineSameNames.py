import json
from unidecode import unidecode
filename = "Turkey_All.json"

#Changes Turkish letters to english, lowercases and adds a hashtag 
with open(filename, "r") as jsonFile:
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
        json.dump(arrLowercase, open('Turkey_All_Lowerscased.json','w'))