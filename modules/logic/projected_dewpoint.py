import pandas as pd
import modules.projection_api as api

def calculate(location, query_type, year, rolling_average):

    raw_projection_df = api.retrieveData(location, query_type, f"{year}-01-02", "2080-12-31")

    # Process projected data
    raw_projection_df['datetime'] = pd.to_datetime(raw_projection_df['datetime'])
    raw_projection_df['year'] = raw_projection_df['datetime'].dt.year
    data_frame = raw_projection_df[['year','data']]
    
    # # Rename column to align with historical data
    data_frame.rename(columns={'data': query_type}, inplace=True)
    data_frame[query_type] = data_frame[query_type].round(4)

    data_frame[f'{rolling_average}_year_rolling_avg'] = data_frame[query_type].rolling(rolling_average).mean().round(4)

    # Drop first X rows that lack a rolling avg
    data_frame = data_frame.iloc[rolling_average:]

    return data_frame
