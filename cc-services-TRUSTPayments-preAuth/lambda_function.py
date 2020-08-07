from modules import simplejson as json
from modules import requests
from modules.cc import helpers
from modules.cc import mappers
import datetime
import sys

def lambda_handler(event, context):
    config = json.loads(helpers.getSSMParameter(mappers.TRUSTPAYMENTS))
    msg = json.loads(event['data'])

    expirydate = str(f"{msg['cardExpirationMonth']:02}") + "/" + str(msg['cardExpirationYear'])

    data = {
          "alias": config['user'],
          "version": config['version'],
          "request": [
            {
              "currencyiso3a": "GBP",
              "requesttypedescriptions": ["ACCOUNTCHECK"],
              "sitereference": config['sitereference'],
              "baseamount": config['baseamount'],
              "orderreference": msg['reference'],
              "accounttypedescription": config['accounttypedescription'],
              "pan": msg['cardNumber'],
              "expirydate": expirydate,
              "securitycode": msg['cardSecurityNumber'],
              "billingpremise": msg['address1'],
              "billingpostcode": msg['postcode']
            }
          ]
        }


    headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
    }

    try:
        response = requests.post(
            config['apiHost'],
            auth=(config['user'], config['password']),
            headers=headers,
            data=json.dumps(data))

        response = json.loads(response.text)
        # print(response.text)
        print('**************************')
        # print(response['response'][0])

        securityresponsesecuritycode  = 0
        securityresponsepostcode = 0
        securityresponseaddress = 0

        if 'response' in response:
            if 'securityresponsesecuritycode' in response['response'][0]:
                securityresponsesecuritycode = response['response'][0]['securityresponsesecuritycode']
            if 'securityresponsepostcode' in response['response'][0]:
                securityresponsepostcode = response['response'][0]['securityresponsepostcode']
            if 'securityresponseaddress' in response['response'][0]:
                securityresponseaddress = response['response'][0]['securityresponseaddress']

            sqs = json.loads(helpers.getSSMParameter(mappers.SQS))
            helpers.sendSQSMessage(sqs[mappers.SQS_CARD_VERIFIED], json.dumps(response))

        if securityresponsesecuritycode == "2" and securityresponsepostcode == "2" and securityresponseaddress == "2":
            result = True
        else:
            result = False


        return {
            'statusCode': 200,
            'body': {'result': result}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': e}
        }