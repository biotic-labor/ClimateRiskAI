from haystack import component
import os
import pandas as pd
import components.climate.geohelper as geo

@component
class ClimateServiceAPIFetcher():

    @component.output_types(dataframe=pd.DataFrame)
    def run(self, location: object, query_type: str) -> pd.DataFrame:
        api_key = os.getenv("CLIMATE_SERVICE_API_KEY")
        latlong = geo.get_lat_long(location)
        start_date = "2024-01-02"
        end_date = "2080-12-31"
        url_dictionary = {
            "num_days_above_100": f"?query=annually(exceed(maxtmp,365,37),mean)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "num_days_above_90": f"?query=annually(exceed(maxtmp,365,32.2),mean)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "num_days_above_80": f"?query=annually(exceed(maxtmp,365,26.7),mean)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "tempmax": f"?query=monthly(maxtmp,max)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "tempmin": f"?query=annually(mintmp,min)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "precip": f"?query=annually(pr,sum)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}",
            "dew":f"?query=annually(dew,mean)&from_date={start_date}T00%3A00%3A00.000Z&to_date={end_date}T00%3A00%3A00.000Z&latitude={latlong[0]}&longitude={latlong[1]}&apikey={api_key}"
            }
        url = f'https://beta.climatedataservice.com/v6/series/csv{url_dictionary[query_type]}'
        df = pd.read_csv(url, skiprows=12)
        df.drop(columns=["latitude", "longitude"], inplace=True, axis=1)
        return {"dataframe":df}