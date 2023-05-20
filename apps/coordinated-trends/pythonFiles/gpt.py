import pandas as pd
import numpy as np
df = pd.DataFrame({'A': [1, 2, np.nan, 4, 5], 'B': [10, 20, np.nan, 40, 50]})

# replace NaN values with 0
#df.fillna(0, inplace=True)

# calculate average of column A
avg_A = df['A'].mean()

# calculate average of column B
avg_B = df['B'].mean()

print('Average of column A:', avg_A)
print('Average of column B:', avg_B)