import boto3

def get_s3_client():
    return boto3.client('s3')

def upload_file_to_s3(file_path, bucket_name, object_name):
    s3 = get_s3_client()
    s3.upload_file(file_path, bucket_name, object_name)

def download_file_from_s3(file_path, bucket_name, object_name):
    s3 = get_s3_client()
    s3.download_file(bucket_name, object_name, file_path)

def upload_chart_data_to_s3(location, query_type):
        # Copy the processed data to the web app
    hyphenated_city = location['city_name'].replace(' ', '-').lower()
    destination_file = open('../../../Climate Platform/ClimatePlatform/data/'+hyphenated_city+'/combined_'+query_type+'.json', 'wb')
    shutil.copyfileobj(source_file, destination_file)
    print('Data copied to web app')
    return True

# bucket_name = 'theworldclimate'
# path = 'climate_data/country_name/city_name'
# file_name = 'combined_data.json'