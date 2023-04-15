import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
filename = r"apps\new-coordinated-trends\data\Turkey.json"
with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        df = pd.DataFrame.from_dict(data, orient='columns')
pd.set_option('display.max_columns', None)

df['sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: [np.nan if v is None else v for v in x])
df['mean_sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: np.mean(np.array(x)))

df['sesLength'] = df['sesLength'].apply(lambda x: [np.nan if v is None else v for v in x])
df['mean_sesLength'] = df['sesLength'].apply(lambda x: np.mean(np.array(x)))
df['total_sesLength'] = df['sesLength'].apply(lambda x: np.sum(np.array(x)))


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
print("Mean session length:", np.mean(allSesLengths))
print("Median session length:", np.median(allSesLengths))
print("Standard deviation of session length:", np.std(allSesLengths))
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
plt.scatter(allSesLengths, allSessionMaxVolumes)
plt.text(1, 8, f"Correlation Coefficient: {corr_coef:.2f}")
plt.title("Correlation between X and Y")
plt.xlabel("ses lengths")
plt.ylabel("max volumes")
plt.show()


plt.scatter(df['mean_sessionMaxVolume'],  df['sesCount'])
plt.title("Correlation between X and Y")
plt.xlabel("mean ses max")
plt.ylabel("ses count")
plt.show()
print("Corr between mean session max volume and session count", df['mean_sessionMaxVolume'].corr(df['sesCount']))
print("Corr between mean session length and session count", df['mean_sesLength'].corr(df['sesCount']))
print("Corr between total session length and session count", df['total_sesLength'].corr(df['sesCount']))
print("Corr between mean session max volume and mean session length", df['mean_sessionMaxVolume'].corr(df['mean_sesLength']))
