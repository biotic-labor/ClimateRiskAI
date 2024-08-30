import pandas as pd

def gics_hydrate():
    df = pd.read_csv('gics-map-2018.csv')
    print(df.tail(20))

gics_hydrate()