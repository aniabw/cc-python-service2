from modules import simplejson as json
from modules import requests
from modules.cc import helpers
from modules.cc import mappers
import urllib.parse

def lambda_handler(event, context):
    config = json.loads(helpers.getSSMParameter(mappers.AXCESS))
    # msg = json.loads(event['data'])
    msg = event['data']

    cardExpiryYear = str(msg['cardExpirationYear'])[-2:]
    customerName = msg['firstName'] + " " + msg['lastName']

    data = {
        'merchantID': config['merchantID'],
        'action': 'VERIFY',
        'amount': config['verifyAmount'],
        'type': config['type'],
        'countryCode': config['countryCode'],
        'currencyCode': config['currencyCode'],
        'cardNumber': msg['cardNumber'],
        'cardExpiryMonth': int(msg['cardExpirationMonth']),
        'cardExpiryYear': int(cardExpiryYear),
        'cardCVV': int(msg['cardSecurityNumber']),
        'transactionUnique': msg['userName'],
        'orderRef': msg['userName'],
        'customerName': customerName,
        'customerEmail': msg['email'],
        'customerPhone': msg['mobilePhone'],
        'customerAddress': msg['address1'],
        'customerPostcode': msg['postcode']
        }

    data['signature'] = helpers.createSignature(data, config['signature'])

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(
            config['apiHost']+"/",
            headers=headers,
            data=data)

        response = urllib.parse.parse_qs(response.text)
        response['reference'] = msg['reference']
        response['userName'] = msg['userName']

        if 'responseCode' in response:
            sqs = json.loads(helpers.getSSMParameter(mappers.SQS))
            helpers.sendSQSMessage(sqs[mappers.SQS_CARD_VERIFIED], json.dumps(response))

        if response['responseCode'][0] == "0":
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
            'body': {'error': e }
        }