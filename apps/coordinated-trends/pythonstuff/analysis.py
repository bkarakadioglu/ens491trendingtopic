import json
import pandas as pd
import numpy as np
filename = r"apps\new-coordinated-trends\data\Turkey.json"
with open(filename, "r") as jsonFile:
        data = json.load(jsonFile)
        df = pd.DataFrame.from_dict(data, orient='columns')
pd.set_option('display.max_columns', None)

df['sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: [np.nan if v is None else v for v in x])
df['mean_sessionMaxVolume'] = df['sessionMaxVolume'].apply(lambda x: np.mean(np.array(x)))

df['sesLength'] = df['sesLength'].apply(lambda x: [np.nan if v is None else v for v in x])
df['mean_sesLength'] = df['sesLength'].apply(lambda x: np.mean(np.array(x)))


#print(df.head())
#The means doesn't include NaN values at all
avg_sessionMaxVolume = df['mean_sessionMaxVolume'].mean()
avg_sesLength = df['mean_sesLength'].mean()

print('Average of mean_sessionMaxVolume:', avg_sessionMaxVolume)
print('Average of mean_sesLength:', avg_sesLength)
print("Number of trends that doesn't have any volume: ", df['mean_sessionMaxVolume'].isna().sum())
print(df.isna().sum())
