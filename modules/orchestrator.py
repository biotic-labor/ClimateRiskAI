import pandas as pd
import sys
import modules.logic.historical_tempmax as hist_tempmax
import modules.logic.historical_tempmin as hist_tempmin
import modules.logic.historical_precip as historical_precip
import modules.logic.historical_dewpoint as hist_dewpoint
import modules.logic.historical_days_above_x as hist_days_above_x
import modules.logic.projected_tempmax as projected_tempmax
import modules.logic.projected_tempmin as projected_tempmin
import modules.logic.projected_days_above_x as projected_days_above_x
import modules.logic.projected_precip as projected_precip
import modules.logic.projected_dewpoint as projected_dewpoint
import modules.logic.combined_rolling_average as combined_rolling_average
def orchestrate(location, query_type, rolling_average):

    year = 2024
    rolling_average_year = 2024-rolling_average
    # Call methodologies
    if(query_type == 'tempmax'):
        print('tempmax')
        # historical_df = hist_tempmax.calculate(raw_historical_df, query_type, rolling_average)
        projected_df = projected_tempmax.calculate(location, query_type, rolling_average_year, rolling_average)
    elif(query_type == 'tempmin'):
        # historical_df = hist_tempmin.calculate(raw_historical_df, query_type, rolling_average)
        projected_df = projected_tempmin.calculate(location, query_type, rolling_average_year, rolling_average)
    elif(query_type == 'num_days_above_80'):
        # historical_df = hist_days_above_x.calculate(raw_historical_df, query_type, 80)
        projected_df = projected_days_above_x.calculate(location, query_type, year)
    elif(query_type == 'num_days_above_90'):
        # historical_df = hist_days_above_x.calculate(raw_historical_df, query_type, 90)
        projected_df = projected_days_above_x.calculate(location, query_type, year)
    elif(query_type == 'num_days_above_100'):
        # historical_df = hist_days_above_x.calculate(raw_historical_df, query_type, 100)
        projected_df = projected_days_above_x.calculate(location, query_type, year)
    elif(query_type == 'precip'):
        # historical_df = historical_precip.calculate(raw_historical_df, rolling_average)
        projected_df = projected_precip.calculate(location, query_type, rolling_average_year, rolling_average)
    elif(query_type == 'dew'):
        # historical_df = hist_dewpoint.calculate(raw_historical_df, year)
        projected_df = projected_dewpoint.calculate(location, query_type, rolling_average_year, rolling_average)

    # # Save the processed data
    # process_historical(location, query_type, historical_df)
    # process_combined(combined_output_location, historical_df, projected_df, rolling_average, query_type)
    # webapp_data_copier.copy(location, combined_output_location, query_type)
    results = process_projected(location, query_type, projected_df)
    return results

# def process_historical(location, query_type, historical_df):
#     historical_output_location = '../'+location['city_name']+'/Processed/historical_'+query_type
#     historical_df.to_csv(historical_output_location+'.csv')
#     historical_df.to_json(historical_output_location+'.json', orient='table')
#     return True

def process_projected(location, query_type, projected_df):
   return projected_df.to_json(orient='table')

# def process_combined(combined_output_location, historical_df, projected_df, rolling_average, query_type):
#     combined_df = pd.concat([historical_df, projected_df])
#     # Add rolling average in that uses combined data
#     combined_df = combined_rolling_average.calculate(combined_df, rolling_average, query_type)
#     combined_df.to_csv(combined_output_location+'.csv')
#     combined_df.to_json(orient='table')
#     return True

