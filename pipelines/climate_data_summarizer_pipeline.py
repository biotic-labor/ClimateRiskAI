import warnings
from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators.openai import OpenAIGenerator
import json
import pandas as pd

from models.querytype import QueryType

warnings.filterwarnings('ignore')
load_env()

def summarize_climate_data(dataframe:pd.DataFrame, query_type:QueryType, industry:str):
    template=f"""You are a climate scientist. You will be given a dataframe with the following columns:datetime, data 
                where datetime represents a year in the future and data represents projected {query_type.prompt_value} for that year.
                Analyze the data over the entire date range, provide analysis and climate risks related to that analysis. Calculate the rate of change of the data over the entire date range, provide output.
                Also, list 5 suggestions for how to prepare a business owner who's industry is in {industry} projected change to the {query_type.prompt_value} in future.
                Provide your response in JSON format similar to the following:{{analysis: string, risks: string, suggestions: string[]}}.
                {{{{dataframe}}}}"""
    
    prompt = PromptBuilder(template=template)
    llm = OpenAIGenerator(model="gpt-4o", generation_kwargs={"response_format":{ "type": "json_object" }})

    climate_suggester = Pipeline()
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("prompt", "llm")
    output = climate_suggester.run({"prompt": {"dataframe": dataframe}})

    return output["llm"]["replies"][0]




