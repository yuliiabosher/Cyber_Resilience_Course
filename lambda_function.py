import boto3
import json
from functions import add_school_data_to_bucket, show_schools_data_in_bucket
def lambda_handler(event, context):
    try:
        filename = "schools_list.csv"
        client = boto3.client('s3')
        # the code executed if Postman sends POST request 
        if event["httpMethod"] == "POST":
            if "body" in event.keys():
                request = event["body"]
                if type(request) is not dict:
                    request = json.loads(request)
                if request is not None and "data" in request.keys():
                    '''if there is no data return a message and an empty list '''
                    data = request["data"]
                    if len(data) == 0:
                        message, return_data = "Please enter valid data", []
                        statuscode = 404
                    else:
                        # if there is data call the function with the data
                        message, return_data = add_school_data_to_bucket(client, filename, data)
                        statuscode = 200
                else:
                    message, return_data = "Error in the POST request occured", []
                    statuscode = 404
        # the code executed if Postman sends GET request
        elif event["httpMethod"] == "GET":
            message, return_data = show_schools_data_in_bucket(client, filename)
            statuscode = 200
        else:
            message, return_data = "Error occured", []
            statuscode = 404
        return {'statusCode': statuscode,
                'headers': {'Content-Type': 'application/json',
                            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                            'Access-Control-Allow-Methods': 'POST',
                            'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"message": message, "data": return_data})
                }
    except Exception as e:
        return {'statusCode': 404,
                'headers': {'Content-Type': 'application/json',
                            'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
                            'Access-Control-Allow-Methods': 'POST',
                            'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"message": "There was an error", "data": []})
                }