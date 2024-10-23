from typing import List
import warnings
from helper import load_env
import pandas as pd
import service.geohelper as geo
import service.climate_data_service as cds
from pipelines.climate_data_summarizer_pipeline import summarize_climate_data
from pipelines.industry_classifier_pipeline import classify_industry
from pipelines.industry_summary_pipeline import summarize_industry
from pipelines.industry_opportunities_pipeline import generate_impact_and_opportunities
from pipelines.industry_sdg_pipeline import generate_industry_sdgs
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
    QueryType("num_days_above_90", "Number of days above 90 degrees farhenheit", "bar"),
    QueryType("num_days_above_100", "Number of days above 100 degrees farhenheit", "bar"),
    QueryType("precip", "Cumulative Annual precipitation", "line"),
    QueryType("tempmax", "Maximum Temperature", "line"),
    QueryType("tempmin", "Minimum Temperature", "line"),
    QueryType("dew", "Dew Point", "line"),
]

# TODO Allow for passing of specific query types
def execute_location_pipeline(location:Location, classified_industry:str):
    response = Response([])
    for query_type in query_types:
        climate_data = orchestrator.orchestrate(location, query_type.name, 10)
        summary = summarize_climate_data(climate_data, query_type, classified_industry)
        analysis = ClimateAnalysis(location, climate_data, summary, query_type)
        response.analyses.append(analysis)
    return response

def execute_industry_classification_pipeline(industry:str):
    return classify_industry(industry)

def execute_risk_mitigation_pipeline(industry:object):
    subindustry_id = int(industry['subindustry_id'])
    GicsData = pd.read_csv('data/Gics_modified_gpt4_v2.csv')
    print(GicsData.loc[(GicsData['SubIndustryId'] == subindustry_id) | (GicsData['IndustryId'] == subindustry_id)])
    row = GicsData.loc[(GicsData['SubIndustryId'] == subindustry_id) | (GicsData['IndustryId'] == subindustry_id)]
    if row["ClimateRiskMitigation"].empty:
        print("No risks found for industry - "+industry['subindustry']+' - '+industry['subindustry_id'])
        return [{"risk": "No risks found for industry", "impact":"No impact found for industry", "mitigation": "No mitigation found for industry", "opportunities": []}]
    combined = execute_opportunities_pipeline(industry['subindustry'], row['ClimateRiskMitigation'].values[0])
    return combined

def execute_industry_summary_pipeline(sub_industry:str, location:Location):
    return summarize_industry(sub_industry, location['city_name'], location['country_name'])

def execute_opportunities_pipeline(sub_industry:str, risk_results:object):
    return generate_impact_and_opportunities(sub_industry, risk_results)

def execute_sdg_pipeline(sub_industry:str):
    return generate_industry_sdgs(sub_industry)