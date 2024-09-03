import pandas as pd
import json

def gics_hydrate():
    df = pd.read_csv('Gics_modified_gpt4.csv')
    count = 0
    for index, row in df.iterrows():
        try:
            # 
            obj = json.loads(str(row['ClimateRiskMitigation']))
            row['ClimateRiskMitigation'] = str(obj).strip()
            # row['ClimateRiskMitigation'] = row['ClimateRiskMitigation'].replace("\"", "\'")
            if row['ClimateRiskMitigation'][-1] != ']':
                print(row['ClimateRiskMitigation'])
                print(row['ClimateRiskMitigation'].strip())
                count+=1
        except Exception as e: 
            # count+=1
            print(e)
    print(count)
    print(df.head(10))
    # df.to_csv('Gics_modified_gpt4_v2.csv')

gics_hydrate()