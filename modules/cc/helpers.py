import os
import sys
import logging
import boto3
import urllib.parse
import hashlib
from modules import simplejson as json
import datetime

# SSM settings
ssmClient = boto3.client("ssm")

# SQS settings
sqsClient = boto3.client("sqs")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getDatabaseAccessDetails():
    database = json.loads(getSSMParameter("cc-rds-"))

    return {
        "DATABASE_HOST": {"WRITER": database["DATABASE_HOST"]["WRITER"], "READER": database["DATABASE_HOST"]["READER"]},
        "DATABASE_USER_WRITER": database["DATABASE_USER_WRITER"],
        "DATABASE_USER_READER": database["DATABASE_USER_READER"],
        "DATABASE_PASSWORD_WRITER": database["DATABASE_PASSWORD_WRITER"],
        "DATABASE_PASSWORD_READER": database["DATABASE_PASSWORD_READER"],
        "DATABASE_NAME": database["DATABASE_NAME"],
        "DATABASE_PORT": database["DATABASE_PORT"],
    }

def getSSMParameter(parameterName, withEncryption=True):
    env = "dev" if getEnvironment() == "local" else getEnvironment()
    # env = "prod" if getEnvironment() == "local" else getEnvironment()
    parameterName = parameterName + env
    parameterValue = None
    try:
        parameterStack = ssmClient.get_parameter(
            Name=parameterName,
            WithDecryption=withEncryption
        )
        parameterValue = parameterStack["Parameter"]["Value"]
    except Exception as e:
        addLogData('error', 'Error while getting SSM parameter `' + parameterName + '`: {}'.format(e))
        sys.exit()

    return parameterValue

def getEnvironment():
    return os.environ["ENVIRONMENT"]

def addLogData(messageType, message):
    if messageType == "error":
        logger.error(message)
    else:
        logger.info(message)

def createSignature(data, key):
    sorted_dict = dict(sorted(data.items()))
    urlencoded_data = urllib.parse.urlencode(sorted_dict)
    normalised_data = urlencoded_data.replace("%0D%0A", "%0A").replace("%0A%0D", "%0A").replace("%0D", "%0A")
    data_to_hash = normalised_data + key
    hashed_data = hashlib.sha512(data_to_hash.encode())
    return hashed_data.hexdigest()

def sendSQSMessage(queueUrl, message):
    try:
        sqsClient.send_message(QueueUrl=queueUrl, MessageBody=message)
    except Exception as e:
        addLogData('error', 'Error while sending SQS message `' + message + '`: {}'.format(e))
        sys.exit()
    return

def receiveSQSMessages(queueUrl):
    return sqsClient.receive_message(
            QueueUrl=queueUrl,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
    )

def deleteBatchSQSMessages(queueUrl, entries):
    return sqsClient.delete_message_batch(
            QueueUrl=queueUrl, Entries=entries
    )

def deleteSQSMessage(queueUrl, receipt_handle):
    return sqsClient.delete_message(
        QueueUrl=queueUrl,
        ReceiptHandle=receipt_handle
    )
