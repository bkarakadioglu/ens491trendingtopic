import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
filenameTurkey = r"apps\new-coordinated-trends\data\Turkey.json"
filenameAdana = r"apps\new-coordinated-trends\data\Adana.json"
filenameAnkara = r"apps\new-coordinated-trends\data\Ankara.json"
filenameAntalya = r"apps\new-coordinated-trends\data\Antalya.json"
filenameBursa = r"apps\new-coordinated-trends\data\Bursa.json"
filenameDiyarbakir = r"apps\new-coordinated-trends\data\Diyarbakir.json"
filenameEskisehir = r"apps\new-coordinated-trends\data\Eskisehir.json"
filenameGaziantep = r"apps\new-coordinated-trends\data\Gaziantep.json"
filenameIstanbul = r"apps\new-coordinated-trends\data\Istanbul.json"
filenameIzmir = r"apps\new-coordinated-trends\data\Izmir.json"
filenameKayseri = r"apps\new-coordinated-trends\data\Kayseri.json"
filenameKonya = r"apps\new-coordinated-trends\data\Konya.json"
filenameMersin = r"apps\new-coordinated-trends\data\Mersin.json"

filenames = [filenameTurkey, filenameAdana, filenameAnkara,
             filenameAntalya, filenameBursa, filenameDiyarbakir,
             filenameEskisehir, filenameGaziantep, filenameIstanbul,
             filenameIzmir, filenameKayseri, filenameKonya, filenameMersin]

dfTurkey = None
dfAdana = None
dfAnkara = None
dfAntalya = None
dfBursa = None
dfDiyarbakir = None
dfEskisehir  = None
dfGaziantep = None
dfIstanbul = None
dfIzmir = None
dfKayseri = None
dfKonya = None
dfMersin = None
dfs = [dfTurkey, dfAdana, dfAnkara,
             dfAntalya, dfBursa, dfDiyarbakir,
             dfEskisehir, dfGaziantep, dfIstanbul,
             dfIzmir, dfKayseri, dfKonya, dfMersin]
cities = ["Turkey", "Adana", "Ankara",
             "Antalya", "Bursa", "Diyarbakir",
             "Eskisehir", "Gaziantep", "Istanbul",
             "Izmir", "Kayseri", "Konya", "Mersin"]
for i in range(13):
        with open(filenames[i], "r") as jsonFile:
                data = json.load(jsonFile)
                dfs[i] = pd.DataFrame.from_dict(data, orient='columns')

count = 0
for df in dfs:
        print("-------------")
        print(cities[count].upper())
        
        df['sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: [np.nan if v is None else v for v in x])
        df['mean_sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: np.nanmean(np.array(x)))

        df['sesLength'] = df['sesLength'].apply(lambda x: [np.nan if v is None else v for v in x])
        df['mean_sesLength'] = df['sesLength'].apply(lambda x: np.nanmean(np.array(x)))
        df['total_sesLength'] = df['sesLength'].apply(lambda x: np.nansum(np.array(x)))

        #print(df.head())
        #The means doesn't include NaN values at all
        avg_sessionMaxVolume = df['mean_sessionMaxVolume'].mean()
        avg_sesLength = df['mean_sesLength'].mean()

        print("Total number of trends:", df.shape[0])
        print('Average of mean_sessionMaxVolume:', avg_sessionMaxVolume)
        print('Average of mean_sesLength:', avg_sesLength)
        print("Number of trends that doesn't have any volume: ", df['mean_sessionMaxVolume'].isna().sum())

        allSesLengths = [val for sublist in df['sesLength'] for val in sublist]
        allSesLengths = np.array(allSesLengths)
        print("Session count:", allSesLengths.shape[0])
        uniqueSesLength, countsSesLength = np.unique(allSesLengths, return_counts=True)
        sesLengthsDict = dict(zip(uniqueSesLength, countsSesLength))
        print("Sessions with no length meaning they were trending in one asof and weren't in the next one:", sesLengthsDict[2.7777777777777776e-07])
        print("Mean session length:", np.nanmean(allSesLengths))
        print("Median session length:", np.nanmedian(allSesLengths))
        print("Standard deviation of session length:", np.nanstd(allSesLengths))
        print("Minimum session length:", np.min(allSesLengths))
        print("Minimum session length excluding zeros:", list(sesLengthsDict.items())[1][0])
        print("Maximum session length:", np.max(allSesLengths))


        allSessionMaxVolumes = [val for sublist in df['sessionMaxVolume'] for val in sublist]
        allSessionMaxVolumes = np.array(allSessionMaxVolumes)
        print("Non null session max volumes", sum(~np.isnan(allSessionMaxVolumes)))
        print("Null session max volumes", sum(np.isnan(allSessionMaxVolumes)))
        print("Session count:", allSessionMaxVolumes.shape[0])
        print("Mean session max volume:", np.nanmean(allSessionMaxVolumes))
        print("Median session max volume:", np.nanmedian(allSessionMaxVolumes))
        print("Standard deviation of session max volume:", np.nanstd(allSessionMaxVolumes))
        print("Minimum session max volume:", np.nanmin(allSessionMaxVolumes))
        print("Maximum session max volume:", np.nanmax(allSessionMaxVolumes))

        df['sesCount'] = df.apply(lambda row: len(row["sesLength"]), axis=1)
        #Right now corrcoef returns nan, just zip the arrays and delete the non nan arrays
        deletionArr = []
        for i in range(len(allSesLengths)):
                if np.isnan(allSessionMaxVolumes[i]):
                        deletionArr.append(i)
        allSesLengths = np.delete(allSesLengths, deletionArr)
        allSessionMaxVolumes = np.delete(allSessionMaxVolumes, deletionArr)

        corr_coef = np.corrcoef(allSesLengths, allSessionMaxVolumes)[0, 1]

        """ fig, axs = plt.subplots(2, 2, figsize=(8, 8))

        fig.suptitle(cities[count])
        fig.tight_layout(pad=5.0)

        axs[0,0].scatter(allSesLengths, allSessionMaxVolumes)
        axs[0,0].set_title("Session Lengths vs Max Volumes Graph for All Sessions")
        axs[0,0].set_xlabel("Session Lengths")
        axs[0,0].set_ylabel("Session Max Volumes")

        axs[0,1].scatter(df['mean_sessionMaxVolume'],  df['sesCount'])
        axs[0,1].set_title("Mean Session Max Volume vs Session Count Graph for Trends")
        axs[0,1].set_xlabel("Mean Session Max")
        axs[0,1].set_ylabel("Session Count")
        for i in range(len(df['mean_sessionMaxVolume'])):
                if df['mean_sessionMaxVolume'][i] > 1800000 or df['sesCount'][i] > 20:
                        axs[0,1].text(df['mean_sessionMaxVolume'][i], df['sesCount'][i], df['name'][i])

        axs[1,0].scatter(df['mean_sessionMaxVolume'],  df['mean_sesLength'])
        axs[1,0].set_title("Mean Session Max Volume vs Mean Session Length for Trends")
        axs[1,0].set_xlabel("Mean Session Max")
        axs[1,0].set_ylabel("Mean Session Length")
        for i in range(len(df['mean_sessionMaxVolume'])):
                if df['mean_sessionMaxVolume'][i] > 1800000 or  df['mean_sesLength'][i] > 25.5 or (df['mean_sessionMaxVolume'][i] > 1000000 and  df['mean_sesLength'][i] > 15):
                        axs[1,0].text(df['mean_sessionMaxVolume'][i], df['mean_sesLength'][i], df['name'][i])

        axs[1,1].scatter(df['mean_sesLength'],  df['sesCount'])
        axs[1,1].set_title("Mean Session Length vs Session Count for Trends")
        axs[1,1].set_xlabel("Mean Session Length")
        axs[1,1].set_ylabel("Session Count")
        for i in range(len(df['mean_sesLength'])):
                if df['mean_sesLength'][i] > 27 or  df['sesCount'][i] > 50:
                        axs[1,1].text(df['mean_sesLength'][i], df['sesCount'][i], df['name'][i])

        plt.show() """

        print("Corr between mean session max volume and session count", df['mean_sessionMaxVolume'].corr(df['sesCount']))
        print("Corr between mean session length and session count", df['mean_sesLength'].corr(df['sesCount']))
        print("Corr between total session length and session count", df['total_sesLength'].corr(df['sesCount']))
        print("Corr between mean session max volume and mean session length", df['mean_sessionMaxVolume'].corr(df['mean_sesLength']))
        count += 1


for i in range(len(dfs)):
    for j in range(i+1, len(dfs)):
        sameTrends = set(dfs[i]['name']).intersection(set(dfs[j]['name']))
        percentage = len(sameTrends) / len(dfs[i]) * 100
        print(f"Similarity between {cities[i]} and {cities[j]}: {percentage:.2f}%")

sameTrendsPercentageMatrix = np.zeros((len(dfs), len(dfs)))

# fill in the matrix with the percentage values
for i in range(len(dfs)):
    for j in range(i+1, len(dfs)):
        sameTrends = set(dfs[i]['name']).intersection(set(dfs[j]['name']))
        percentage = len(sameTrends) / len(dfs[i]) * 100
        sameTrendsPercentageMatrix[i][j] = percentage
        sameTrendsPercentageMatrix[j][i] = percentage  # set the symmetric value

sns.heatmap(sameTrendsPercentageMatrix, annot=True, fmt=".2f", cmap='YlGnBu',
             xticklabels=cities, yticklabels=cities,
             vmin=95)
plt.title("Percentage of Same Trends in Cities")
plt.show()

sameTrendsForAnkaraAndTurkey = set(dfs[0]['name']).intersection(set(dfs[2]['name']))
differentTrendsInIstanbul = set(dfs[8]['name']).difference(sameTrendsForAnkaraAndTurkey)
print("Different trends in Istanbul", differentTrendsInIstanbul)
