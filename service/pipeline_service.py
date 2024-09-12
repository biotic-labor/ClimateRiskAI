from typing import List
import warnings
from helper import load_env
import pandas as pd
import service.geohelper as geo
import service.climate_data_service as cds
from pipelines.climate_data_summarizer_pipeline import summarize_climate_data
from pipelines.industry_classifier_pipeline import classify_industry
import modules.orchestrator as orchestrator
import models.location as Location
from models.querytype import QueryType
import json
warnings.filterwarnings('ignore')
load_env()

class ClimateAnalysis:
    def __init__(self, location: Location, climate_data: str, summary: str, query_type: QueryType):
        self.location = location
        self.query_type = query_type
        self.climate_data = climate_data
        self.summary = summary

class Response:
    def __init__(self, analyses: List[ClimateAnalysis]):
        self.analyses = analyses


query_types = [
    # QueryType("num_days_above_90", "Number of days above 90 degrees farhenheit"),
    # QueryType("num_days_above_100", "Number of days above 100 degrees farhenheit"),
    # QueryType("precip", "Cumulative Annual precipitation"),
    QueryType("tempmax", "Maximum Temperature"),
    # QueryType("tempmin", "Minimum Temperature"),
    # QueryType("dew", "Dew Point"),
]

# TODO Allow for passing of specific query types
def execute_location_pipeline(location:Location, classified_industry:str):
    response = Response([])
    for query_type in query_types:
        print(query_type.name)
        climate_data = orchestrator.orchestrate(location, query_type.name, 5)
        summary = summarize_climate_data(climate_data, query_type, classified_industry)
        analysis = ClimateAnalysis(location, climate_data, summary, query_type)
        response.analyses.append(analysis)
    return response

def execute_industry_classification_pipeline(industry:str):
    return classify_industry(industry);

def execute_risk_mitigation_pipeline(industry:object):
    subindustry_id = int(industry['subindustry_id'])
    GicsData = pd.read_csv('data/Gics_modified_gpt4_v2.csv')
    print(GicsData.loc[(GicsData['SubIndustryId'] == subindustry_id) | (GicsData['IndustryId'] == subindustry_id)])
    row = GicsData.loc[(GicsData['SubIndustryId'] == subindustry_id) | (GicsData['IndustryId'] == subindustry_id)]
    if row["ClimateRiskMitigation"].empty:
        return {}
    return row['ClimateRiskMitigation'].values[0]