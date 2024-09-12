from flask import Flask, jsonify, request, make_response
import service.pipeline_service as pipeline_service
import subprocess
import jsonpickle
import os
from flask import Flask
from flask_cors import CORS


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
    classified_industry = pipeline_service.execute_industry_classification_pipeline(industry)
    location_results = pipeline_service.execute_location_pipeline(location, classified_industry['subindustry'])
    json_location_results = jsonpickle.encode(location_results, unpicklable=False)

    risk_results = pipeline_service.execute_risk_mitigation_pipeline(classified_industry)
    combined_results = {"locations_results":json_location_results, "risk_results":risk_results}

    return make_response(jsonpickle.encode(combined_results, unpicklable=False), 200)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
