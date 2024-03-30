from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib.parse

print('Loading function')

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# --------------- Helper Functions ------------------

def index_faces(bucket, key):
    response = rekognition.index_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        CollectionId="cricketers"
    )
    return response
    
def update_index(tableName, faceId, fullName):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName}
        }
    ) 
    
# --------------- Main handler ------------------

def lambda_handler(event, context):
    try:
        # Get the object from the event
        records = event.get('Records', [])
        if not records:
            print("No records found in the event.")
            return {'statusCode': 400, 'body': 'No records found in the event.'}

        record = records[0]  # Assuming only one record for simplicity
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        print("Processing object: s3://{}/{}".format(bucket, key))

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object
        response = index_faces(bucket, key)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            face_records = response.get('FaceRecords', [])
            if not face_records:
                print("No faces detected in the image.")
                return {'statusCode': 400, 'body': 'No faces detected in the image.'}

            faceId = face_records[0]['Face']['FaceId']
            object_metadata = s3.head_object(Bucket=bucket, Key=key)
            person_full_name = object_metadata['Metadata'].get('fullname', 'Unknown')

            update_index('cricketers_collection', faceId, person_full_name)

            print("Face indexed successfully. FaceId: {}, Full Name: {}".format(faceId, person_full_name))
            return {'statusCode': 200, 'body': 'Face indexed successfully.'}
        else:
            print("Error indexing faces. Response: {}".format(response))
            return {'statusCode': 500, 'body': 'Error indexing faces.'}
    except Exception as e:
        print("Error processing object {}: {}".format(key, e))
        return {'statusCode': 500, 'body': 'Error processing object: {}'.format(e)}
