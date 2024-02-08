import json
from functions import get_S3_client, get_file

def lambda_handler(event, context):
  try:
    request = event["body"]
    if type(request) is not dict:
      request = json.loads(request)
    data = request["data"]
    csv_filename = data["csv_filename"]
    resource = get_S3_client()
    return_data = get_file(resource, csv_filename)
    return {
        "statusCode": 200,
        "headers":{
            "Content-Type" : "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Api-Key",
            "Access-Control-Allow-Methods" : "POST",
            "Access-Control-Allow-Origin":"*"
        },
        "body": json.dumps(return_data),
    }
  except Exception as e:
    return {
        "statusCode": 404,
        "headers":{
            "Content-Type" : "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Api-Key",
            "Access-Control-Allow-Methods" : "POST",
            "Access-Control-Allow-Origin":"*"
        },
        "body": f"there was an error, {e}"
    }
