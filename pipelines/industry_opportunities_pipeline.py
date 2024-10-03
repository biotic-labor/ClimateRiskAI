from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
import json
from pydantic import BaseModel

class ImpactAndOpportunities(BaseModel):
    risk:str
    mitigation:str
    impact:str
    opportunities:list[str]

load_env()

def generate_impact_and_opportunities(sub_industry:str, risk_results:dict):
    prompt_template="""Provide an example of an impact that may occur as a result of {{risk}} in the industry of {{sub_industry}}, also List 3 tangible ways a business owner could {{mitigation}} in the industry of {{sub_industry}}. Provide your response in the JSON format impact:string, opportunities:[string,string,string]"""
    
    prompt = PromptBuilder(template=prompt_template)

    model_schema = ImpactAndOpportunities.model_json_schema()
    llm = OpenAIGenerator(model="gpt-4o-mini", generation_kwargs={"response_format":{ "type": "json_object" }})

    climate_suggester = Pipeline()
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("prompt", "llm")
    response = []
    risks = json.loads(risk_results)
    for risk in risks:
        output = climate_suggester.run({"prompt": {"sub_industry":sub_industry,"mitigation": risk['mitigation']}})
        impact_and_opportunities = json.loads(output["llm"]["replies"][0])
        response.append({
            'risk':risk['risk'],
            'mitigation':risk['mitigation'],
            'impact':impact_and_opportunities['impact'],
            'opportunities':impact_and_opportunities['opportunities']
        })
    return response