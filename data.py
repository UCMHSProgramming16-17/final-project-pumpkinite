import pandas as pd
from bokeh.sampledata.us_states import data as states

df = pd.read_csv('prescriber-info.csv')


prescriptions = {}

df["Total"] = 1

print(df.head(1))

#for code in states:
    
#    prescriptions[code] = 