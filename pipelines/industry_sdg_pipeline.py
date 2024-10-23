from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
import json

load_env()

def generate_industry_sdgs(sub_industry:str):
    prompt_template="""what would be the top 4 SDGs for the {{sub_industry}} and how do they relate to my specific industry, please provide the response and in json format like "top_sdgs":[{"sdg":"string", "description":"string", "industry_relation":"string"}]"""
    
    prompt = PromptBuilder(template=prompt_template)

    llm = OpenAIGenerator(model="gpt-4o-mini", generation_kwargs={"response_format":{ "type": "json_object" }})

    climate_suggester = Pipeline()
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("prompt", "llm")
    sdg_result = climate_suggester.run({"prompt": {"sub_industry":sub_industry}})
    return json.loads(sdg_result["llm"]["replies"][0])