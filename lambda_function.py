import json
from functions import divide_numbers, multiply_numbers, add_numbers, subtract_numbers

def lambda_handler(event, context):
  try:
    request = event["body"]
    if type(request) is not dict:
      request = json.loads(request)
    data = request["data"]
    operation = data["operation"]
    num1 = data["num1"]
    num2 = data["num2"]
    if operation=="add":
      return_data = add_numbers(num1, num2)
    elif operation=="multiply":
      return_data=multiply_numbers(num1, num2)
    elif operation=="subtract":
      return_data=subtract_numbers(num1, num2)
    elif operation=="divide":
      return_data=divide_numbers(num1, num2)
    else: 
      return {
        "statusCode": 404,
        "headers":{
            "Content-Type" : "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Api-Key",
            "Access-Control-Allow-Methods" : "POST",
            "Access-Control-Allow-Origin":"*"
        },
        "body": "invalid operation or number",
    }
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
  except:
    return {
        "statusCode": 404,
        "headers":{
            "Content-Type" : "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Api-Key",
            "Access-Control-Allow-Methods" : "POST",
            "Access-Control-Allow-Origin":"*"
        },
        "body": "error",
    }
