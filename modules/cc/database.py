import sys
from modules import simplejson as json
from modules.cc import helpers
import pyodbc

databaseDetails = helpers.getDatabaseAccessDetails()

hostWriter = databaseDetails["DATABASE_HOST"]["WRITER"]
userWriter = databaseDetails["DATABASE_USER_WRITER"]
passwdWriter = databaseDetails["DATABASE_PASSWORD_WRITER"]
hostReader = databaseDetails["DATABASE_HOST"]["READER"]
userReader = databaseDetails["DATABASE_USER_READER"]
passwdReader = databaseDetails["DATABASE_PASSWORD_READER"]
db = databaseDetails["DATABASE_NAME"]
port = databaseDetails["DATABASE_PORT"]

try:
    helpers.addLogData("info", "Starting WRITER connection")
    connWriter = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + hostWriter + ';DATABASE=' + db + ';UID=' + userWriter + ';PWD=' + passwdWriter)
except Exception as error:
    helpers.addLogData("error", "MsSQL WRITER connection error: " + str(error))
    sys.exit()

try:
    helpers.addLogData("info", "Starting READER connection")
    connReader = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + hostReader + ';DATABASE=' + db + ';UID=' + userReader + ';PWD=' + passwdReader)
except Exception as error:
    helpers.addLogData("error", "MsSQL WRITER connection error: " + str(error))
    sys.exit()


def getConnWriter():
    return connWriter


def getConnReader():
    return connReader

def getCampaign():
    try:
        cursor = connReader.cursor()
        cursor.execute("SELECT * FROM campaign")
        return cursor.fetchall()
    except Exception as e:
        helpers.addLogData(
            "error", "Error while finding campaign. MsSQL Error: {}".format(e)
        )
        sys.exit()

def createPreAuthResponse(data):
    try:
        sql = "INSERT INTO preauthresponse (reference, cv2check, cardtype, cardscheme, transactionid, type, amount, merchantID, threeDSCheckPref, cv2CheckPref, addressCheckPref, postcodeCheckPref, merchantCategoryCode, action, requestID, merchantAlias, responseCode, responseMessage, state, requestMerchantID, processMerchantID, xref, paymentMethod, authorisationCode, responseStatus, timestamp, amountReceived, avscv2ResponseCode, avscv2ResponseMessage, avscv2AuthEntity, addressCheck, postcodeCheck, cardTypeCode, cardSchemeCode, cardIssuer, cardIssuerCountry, cardIssuerCountryCode, vcsResponseCode, vcsResponseMessage, responsetimestamp, username) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor = connWriter.cursor()
        cursor.execute(
            sql,
            (
                data['reference'] if 'reference' in data else '',
                data['cv2Check'][0] if 'cv2Check' in data else '',
                data['cardType'][0] if 'cardType' in data else '',
                data['cardScheme'][0] if 'cardScheme' in data else '',
                data['transactionID'][0] if 'transactionID' in data else '',
                data['type'][0] if 'type' in data else '',
                data['amount'][0] if 'amount' in data else '',
                data['merchantID'][0] if 'merchantID' in data else '',
                data['threeDSCheckPref'][0] if 'threeDSCheckPref' in data else '',
                data['cv2CheckPref'][0] if 'cv2CheckPref' in data else '',
                data['addressCheckPref'][0] if 'addressCheckPref' in data else '',
                data['postcodeCheckPref'][0] if 'postcodeCheckPref' in data else '',
                data['merchantCategoryCode'][0] if 'merchantCategoryCode' in data else '',
                data['action'][0] if 'action' in data else '',
                data['requestID'][0] if 'requestID' in data else '',
                data['merchantAlias'][0] if 'merchantAlias' in data else '',
                data['responseCode'][0] if 'responseCode' in data else '',
                data['responseMessage'][0] if 'responseMessage' in data else '',
                data['state'][0] if 'state' in data else '',
                data['requestMerchantID'][0] if 'requestMerchantID' in data else '',
                data['processMerchantID'][0] if 'processMerchantID' in data else '',
                data['xref'][0] if 'xref' in data else '',
                data['paymentMethod'][0] if 'paymentMethod' in data else '',
                data['authorisationCode'][0] if 'authorisationCode' in data else '',
                data['responseStatus'][0] if 'responseStatus' in data else '',
                data['timestamp'][0] if 'timestamp' in data else '',
                data['amountReceived'][0] if 'amountReceived' in data else '',
                data['avscv2ResponseCode'][0] if 'avscv2ResponseCode' in data else '',
                data['avscv2ResponseMessage'][0] if 'avscv2ResponseMessage' in data else '',
                data['avscv2AuthEntity'][0] if 'avscv2AuthEntity' in data else '',
                data['addressCheck'][0] if 'addressCheck' in data else '',
                data['postcodeCheck'][0] if 'postcodeCheck' in data else '',
                data['cardTypeCode'][0] if 'cardTypeCode' in data else '',
                data['cardSchemeCode'][0] if 'cardSchemeCode' in data else '',
                data['cardIssuer'][0] if 'cardIssuer' in data else '',
                data['cardIssuerCountry'][0] if 'cardIssuerCountry' in data else '',
                data['cardIssuerCountryCode'][0] if 'cardIssuerCountryCode' in data else '',
                data['vcsResponseCode'][0] if 'vcsResponseCode' in data else '',
                data['vcsResponseMessage'][0] if 'vcsResponseMessage' in data else '',
                data['timestamp'][0] if 'timestamp' in data else '',
                data['userName'] if 'userName' in data else ''
            ),
        )
        cursor.commit()
        return True
    except Exception as e:
        helpers.addLogData(
            "error",
            "Error while creating preauthresponse. MsSQL Error: {}".format(
                e
            ),
        )
        sys.exit()