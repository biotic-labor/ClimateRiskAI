import pandas as pd
import json

def gics_hydrate():
    df = pd.read_csv('Gics_modified.csv')
    count = 0
    for index, row in df.iterrows():
        try:
            row['climate_risk'] = row['climate_risk'].replace("'", "\"")
            json.loads(str(row['climate_risk']))
        except Exception as e: 
            count+=1
            print(e)
            print(row['SubIndustryDescription'])
    print(count)

gics_hydrate()