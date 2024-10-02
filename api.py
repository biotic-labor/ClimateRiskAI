from flask import Flask, jsonify, request, make_response
import service.pipeline_service as pipeline_service
import subprocess
import jsonpickle
import os
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    secret = data.get("secret")
    if(secret != "magic"):
        return make_response(jsonify({"error": "Invalid secret"}), 401)
    location = data.get("location")
    industry = data.get("industry")
    mock = data.get("mock")
    if(mock):
        with open('mock_data.json', 'r') as file:
            mock_data = json.load(file)
        print('using mock data')
        return make_response(mock_data, 200)
    industry_results = pipeline_service.execute_industry_classification_pipeline(industry)
    industry_summary = pipeline_service.execute_industry_summary_pipeline(industry, location)
    location_results = pipeline_service.execute_location_pipeline(location, industry_results['subindustry'])
    risk_results = pipeline_service.execute_risk_mitigation_pipeline(industry_results)
    combined_results = {"industry_info":industry_results, "industry_summary":industry_summary, "locations_results":location_results, "risk_results":risk_results}
    with open('mock_data.json', 'w') as f:
        json.dump(jsonpickle.encode(combined_results, unpicklable=False), f)
    response =  make_response(jsonpickle.encode(combined_results, unpicklable=False), 200)
    print(response)
    return response

@app.route('/classify', methods=['GET'])
def classify():
    industry = request.args.get('industry')
    return make_response(jsonify(pipeline_service.execute_industry_classification_pipeline(industry)), 200)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
