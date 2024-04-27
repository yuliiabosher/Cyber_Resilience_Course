import os
import boto3
import json
import csv
import botocore

def add_school_data_to_bucket(client, filename, filedata):
    try:
        s3_client = boto3.client('s3')
        s3 = boto3.resource('s3')
        # access the bucket using the environment variable
        bucket = s3.Bucket(os.environ.get("BUCKET_NAME"))
        # read the file from the bucket 
        obj = s3_client.get_object(Bucket=os.environ.get("BUCKET_NAME"), Key=filename)
        data = obj['Body'].read().decode('utf-8').splitlines()
        records = csv.reader(data) 
        names_array = []
        # create a file in a temporary folder and write the bucket file contents in it 
        with open('/tmp/schools_list.csv', 'w', newline='') as f:
            for row in records:
                names_array.append(row[0])
                writer = csv.writer(f)
                writer.writerow(row)
        new_data_rows = []
        # append the schools not in bucket file to the file in the temporary folder 
        with open('/tmp/schools_list.csv', 'a', newline='') as f:
            for i in filedata:
                if i[0] not in names_array:
                    new_data_rows.append(i)
                    writer = csv.writer(f)
                    writer.writerow(i)
        if len(new_data_rows) == 0:
            return "These schools are already in a file", []
        else:
            # upload the file from the temporary folder to the bucket '''
            bucket.upload_file('/tmp/schools_list.csv', filename)
            return "New data been successfully added", new_data_rows
    except botocore.exceptions.ClientError as e:
        # if the file doesn't exist create a new file in the temporary folder
        if e.response["Error"]["Code"] == "NoSuchKey":
            with open('/tmp/schools_list.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                for row in filedata:
                    writer.writerow(row)
            # upload the file from the temporary folder to the bucket
            bucket.upload_file('/tmp/schools_list.csv', filename)
            return "New file been successfully created", filedata
        else:
            return e.response["Error"]["Code"], []
            
def show_schools_data_in_bucket(client, filename):
    try: 
        s3_client = boto3.client('s3')
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.environ.get("BUCKET_NAME"))
        # read and return data from the bucket 
        obj = s3_client.get_object(Bucket=os.environ.get("BUCKET_NAME"), Key=filename)
        data = obj['Body'].read().decode('utf-8').splitlines()
        records = csv.reader(data) 
        data_array =[]
        for row in records:
            data_array.append(row)
        return "The data has been found", data_array
    except botocore.exceptions.ClientError as e:
        # if there is no file in bucket return a message and an empty list
        if e.response["Error"]["Code"] == "NoSuchKey":
            return "There is no such file", []
        else:
            return e.response["Error"]["Code"], []
    except:
        return "There was an error", []
    
    
    