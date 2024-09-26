from helper import load_env
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
import json

load_env()

def generate_opportunities(sub_industry:str, risk_results:dict):
    prompt_template="""List 1 to 3 tangible ways someone could {{mitigation}} in the industry of {{sub_industry}}. Provide your response in the JSON format [string,string,string]"""
    
    prompt = PromptBuilder(template=prompt_template)
    llm = OpenAIGenerator()

    climate_suggester = Pipeline()
    climate_suggester.add_component("prompt", prompt)
    climate_suggester.add_component("llm", llm)

    climate_suggester.connect("prompt", "llm")
    response = []
    risks = json.loads(risk_results)
    for risk in risks:
        output = climate_suggester.run({"prompt": {"sub_industry":sub_industry,"mitigation": risk['mitigation']}})
        opportunities = json.loads(output["llm"]["replies"][0])
        response.append({
            'risk':risk['risk'],
            'mitigation':risk['mitigation'],
            'opportunities':opportunities
        })
    return response