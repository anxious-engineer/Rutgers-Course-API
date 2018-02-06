import sys
import pymongo

# AWS Lambda Function that handles method triggers from the API Gateway.
# Specifically used in the RU CAPI PoC
PASSWORD = "makingausableapi"
uri = "mongodb+srv://admin:" + PASSWORD + "@poc-5vbvd.mongodb.net/test"
DB = "PoC"
coll = "12018"

def api_handler(event, context):

    # Connect to Mongo Cluster
    client = pymongo.MongoClient(uri)

    query_params = event.get("queryStringParameters")

    if query_params:
        new_params = {
            "SEMESTER" : query_params.get('semester'),
            "LEVEL" : query_params.get('level'),
            "SUBJECT" : query_params.get('subject'),
            "CAMPUS" : query_params.get('campus')
        }
        query_params = new_params
    else:
        query_params = {}

    doc = client[DB][coll].find_one(query_params)

    body = doc.get("DATA") if doc else str(doc)

    # Close Mongo Connection
    close_response = client.close()
    response = {
        "statusCode": 200,
        "headers": {
        },
        "body": str(body),
        "isBase64Encoded": False
    };
    return response
