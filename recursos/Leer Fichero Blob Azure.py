import pandas as pd 
ruta = 'https://stgdemodata.blob.core.windows.net/files/weblogs/weblogs.csv'
df= pd.read_csv (ruta)
df.head()
