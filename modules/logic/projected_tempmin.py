import pandas as pd
import modules.projection_api as api

def calculate(location, query_type, year, rolling_average):

    # Retrieve the projected data
    raw_projection_df = api.retrieveData(location, query_type, f"{year}-01-02", "2080-12-31")

    # Process projected data
    data_frame = raw_projection_df[['datetime','data']]
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'])
    data_frame = data_frame.groupby([pd.Grouper(key='datetime', freq='1YE')],as_index=False).min()
    data_frame['datetime'] = pd.to_datetime(data_frame['datetime'])
    data_frame['year'] = data_frame['datetime'].dt.year

    # Rename column to align with historical data
    data_frame.rename(columns={'data': query_type}, inplace=True)

    # Calculate Yearly Rolling Average
    data_frame[f'{rolling_average}_year_rolling_avg'] = data_frame[query_type].rolling(rolling_average).mean().round(2)

    # Drop first X rows that lack a rolling avg
    data_frame = data_frame.iloc[rolling_average:]

    return data_frame