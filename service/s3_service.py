import boto3
import json
import os

def get_s3_client():
    return boto3.client('s3')

def download_company_report_from_s3(company_name, location, industry):
    s3 = get_s3_client()
    bucket_name = 'theworldclimate'
    file_name = 'report_data/'+company_name+'/'+industry+'/'+location['country_name']+'/'+location['city_name']+'/'+company_name+'_report.json'
    print('downloading - '+file_name)
    try:
        s3_response_object = s3.get_object(Bucket=bucket_name, Key=file_name)
        object_content = s3_response_object['Body'].read().decode('utf-8')
        json_content = json.loads(object_content)
        return json_content   
    except Exception as e:
        return None

def upload_company_report_to_s3(company_name, location, industry, report_data):
    s3 = get_s3_client()
    bucket_name = 'theworldclimate'
    file_name = 'report_data/'+company_name+'/'+industry+'/'+location['country_name']+'/'+location['city_name']+'/'+company_name+'_report.json'
    s3.put_object(Body=bytes(json.dumps(report_data).encode('UTF-8')), Bucket=bucket_name, Key=file_name)

# bucket_name = 'theworldclimate'
# path = 'climate_data/country_name/city_name'
# file_name = 'combined_data.json'