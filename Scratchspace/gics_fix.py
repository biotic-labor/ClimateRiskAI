import pandas as pd
import json

def gics_hydrate():
    df = pd.read_csv('Gics_modified_gpt4.csv')
    count = 0
    for index, row in df.iterrows():
        try:
            # 
            obj = json.loads(str(row['ClimateRiskMitigation']))
            df.at[row.name,'ClimateRiskMitigation'] = str(obj)
            row['ClimateRiskMitigation'] = row['ClimateRiskMitigation'].replace("'", "\"")
            print(obj)
        except Exception as e: 
            count+=1
            print(e)
            print(row['SubIndustryDescription'])
    print(count)
    print(df.head(10))
    df.to_csv('Gics_modified_gpt4_v2.csv')

gics_hydrate()