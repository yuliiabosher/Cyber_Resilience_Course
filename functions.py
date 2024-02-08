import os
import boto3

def get_S3_client():
  resource = boto3.client("s3")
  return resource
def get_file(client, filename):
  file_object = client.get_object(Bucket=os.environ.get('BUCKET_NAME'), Key=filename)
  data_file = file_object['Body'].read()
  return str(data_file.decode('utf-8'))

  
