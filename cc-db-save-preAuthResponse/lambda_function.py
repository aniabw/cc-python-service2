from modules import simplejson as json
from modules import requests
from modules.cc import helpers
from modules.cc import mappers
from modules.cc import database
import urllib.parse

def lambda_handler(event, context):

    for message in event["Records"]:
        data = json.loads(message["body"])

        try:
            database.createPreAuthResponse(data)

            return {
                'statusCode': 200
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': {'error': e }
            }