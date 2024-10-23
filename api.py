from flask import Flask, jsonify, request, make_response
import service.pipeline_service as pipeline_service
import service.s3_service as s3_service
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
    company_name = data.get("company_name")
    existing_data = s3_service.download_company_report_from_s3(company_name, location, industry)
    if(existing_data):
        return make_response(existing_data, 200)
    # mock = data.get("mock")
    # if(mock):
    #     with open('mock_data.json', 'r') as file:
    #         mock_data = json.load(file)
    #     print('using mock data')
    #     return make_response(mock_data, 200)
    industry_results = pipeline_service.execute_industry_classification_pipeline(industry)
    industry_summary = pipeline_service.execute_industry_summary_pipeline(industry, location)
    location_results = pipeline_service.execute_location_pipeline(location, industry_results['subindustry'])
    risk_results = pipeline_service.execute_risk_mitigation_pipeline(industry_results)
    sdg_results = pipeline_service.execute_sdg_pipeline(industry_results['subindustry'])
    combined_results = {"industry_info":industry_results, "industry_summary":industry_summary, "locations_results":location_results, "risk_results":risk_results, "sdg_results":sdg_results}
    # with open('mock_data.json', 'w') as f:
    #     json.dump(jsonpickle.encode(combined_results, unpicklable=False), f)
    jsonData = jsonpickle.encode(combined_results, unpicklable=False)
    s3_service.upload_company_report_to_s3(company_name, location, industry, jsonData)
    response =  make_response(jsonData, 200)
    print(response)
    return response

@app.route('/classify', methods=['GET'])
def classify():
    industry = request.args.get('industry')
    return make_response(jsonify(pipeline_service.execute_industry_classification_pipeline(industry)), 200)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
