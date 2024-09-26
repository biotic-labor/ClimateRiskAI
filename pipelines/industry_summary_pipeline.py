from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
import json

load_env()

def summarize_industry(sub_industry:str, city_name:str, country_name:str):
    print(sub_industry, city_name, country_name)
    prompt_template="""You are a climate scientist who is analyzing how climate change may impact a specific industry.
                Summarize how the changing climate could impact this industry {{industry}} in the city of {{city}} in the country of {{country}}. 
                Include information related to that industry's supply chain, natural resource requirements, operations, and other relevant factors such as geographic location and relevant climate events that have occured in {city_name} in the last 10 years.
                Provide your response in the JSON format industry_summary: string"""
    
    prompt = PromptBuilder(template=prompt_template)
    llm = OpenAIGenerator()

    climate_suggester = Pipeline()
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("prompt", "llm")

    output = climate_suggester.run({"prompt": {"industry": sub_industry, "city": city_name, "country": country_name}})
    return json.loads(output["llm"]["replies"][0])