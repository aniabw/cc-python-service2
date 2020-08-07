import local_env
import sys
import importlib

# lambda_function = importlib.import_module("cc-services-axcess-preAuth.lambda_function")
# lambda_function = importlib.import_module("cc-db-save-preAuthResponse.lambda_function")

lambda_function = importlib.import_module("cc-services-TRUSTPayments-preAuth.lambda_function")
try:
    event = sys.argv[1]
except IndexError:
    # send-exported-data-to-provider
    # event = {
    #   "key1": "value1",
    #   "key2": "value2",
    #   "key3": "value3"
    # }

    # InstID = Utils.getPrivateSetting("InstID");
    # SignatureKey = Utils.getPrivateSetting("SignatureKey");
    # APIPreauth = Utils.getPublicSetting("APIPreauth");
    # PingAmount = Utils.getPublicSetting("PingAmt");
    # TransactionType = "VERIFY";
    # TransactionId = "1";
    # Currency = "826";
    # Country = "826";

    # event = {
    #     "Records": [{
    #         "messageId": "6abd8bca-da4d-4e80-9260-c64953a4383e",
    #         "receiptHandle":
    #             "AQEB7b3pJbecFIFjILb5kV3y4OFcqTnRyqtuYppoutcDHfXzCvi7E6aoSHT/LPI49kkCsxZrPyiteDL+Pk7hvwgWPLd1G8YsIsuD0eQ58HyH6WNuNqAK9h0aah6GTYChNJtKAOC1d/5sgU/vyOOWvQqyw6ts3KTDjBA88IFEfwNhFrSscLOabZl1PYmMtH0vvi8S4VpwbLrnEewOb++XNbCYdSfEaPj6K4kZFwKgiH994LEH47wBlYGaebMEKa+ODqfXVx96ry5pFUbWcMzPE1s7V1qW7ldY5999q/703VMVM1fCb7Gll1AF97sv0BX0QbKcgxnfo6C9UIX5gMoa33WNPGwG38s3Ieg86TB0xR7UgN5Yktu1WPm6EmR5feCtkRwXbTamKkuEMRzbnnZnFw4ufw==",
    #         "body":
    #             "{\"paymentData\":{\"amount\":0,\"type\":1,\"countryCode\":826,\"currencyCode\":826,\"cardNumber\":\"4012002222222222\",\"cardExpiryMonth\":12,\"cardExpiryYear\":23,\"cardCVV\":\"083\",\"transactionUnique\":76961246,\"orderRef\":\"Test purchase\",\"customerName\":\"Test Customer\",\"customerEmail\":\"test@testcustomer.com\",\"customerPhone\":\"+44 (0) 123 45 67 890\", \"customerAddress\":\"16 Test Street\", \"customerPostcode\":\"TE15 5ST\", \"reference\":\"number\"}}",
    #         "attributes": {
    #             "ApproximateReceiveCount": "1",
    #             "SentTimestamp": "1575475031083",
    #             "SenderId": "AKIA4T2RH2EKQWEICEFX",
    #             "ApproximateFirstReceiveTimestamp": "1575475031089"
    #         },
    #         "messageAttributes": {},
    #         "md5OfBody": "e7dfba465de78617df5d0752c74f5297",
    #         "eventSource": "aws:sqs",
    #         "eventSourceARN":
    #             "arn:aws:sqs:eu-west-2:389139102731:dev-application-created",
    #         "awsRegion": "eu-west-1"
    #     }
    #     ]
    # }

    # event = {
    #     "Records": [{
    #         "messageId": "6abd8bca-da4d-4e80-9260-c64953a4383e",
    #         "receiptHandle":
    #             "AQEB7b3pJbecFIFjILb5kV3y4OFcqTnRyqtuYppoutcDHfXzCvi7E6aoSHT/LPI49kkCsxZrPyiteDL+Pk7hvwgWPLd1G8YsIsuD0eQ58HyH6WNuNqAK9h0aah6GTYChNJtKAOC1d/5sgU/vyOOWvQqyw6ts3KTDjBA88IFEfwNhFrSscLOabZl1PYmMtH0vvi8S4VpwbLrnEewOb++XNbCYdSfEaPj6K4kZFwKgiH994LEH47wBlYGaebMEKa+ODqfXVx96ry5pFUbWcMzPE1s7V1qW7ldY5999q/703VMVM1fCb7Gll1AF97sv0BX0QbKcgxnfo6C9UIX5gMoa33WNPGwG38s3Ieg86TB0xR7UgN5Yktu1WPm6EmR5feCtkRwXbTamKkuEMRzbnnZnFw4ufw==",
    #         "body":
    #             "{\"responseCode\":[\"65559\"],\"responseMessage\":[\"ERROR CODE (RC_IP_BLOCKED_SECONDARY)\"],\"responseStatus\":[\"2\"],\"__wafRequestID\":[\"2020-07-10T10:04:02Z|9ab22fa831|35.179.78.6|1UMjFl4UTD\"],\"merchantID\":[\"122365\"],\"action\":[\"VERIFY\"],\"amount\":[\"0\"],\"type\":[\"1\"],\"countryCode\":[\"826\"],\"currencyCode\":[\"826\"],\"cardExpiryMonth\":[\"12\"],\"cardExpiryYear\":[\"23\"],\"transactionUnique\":[\"76961246\"],\"orderRef\":[\"Test purchase\"],\"customerName\":[\"Test Customer\"],\"customerEmail\":[\"test@testcustomer.com\"],\"customerPhone\":[\"+44 (0) 123 45 67 890\"],\"customerAddress\":[\"16 Test Street\"],\"customerPostcode\":[\"TE15 5ST\"],\"requestID\":[\"5f083d12d823a\"],\"merchantAlias\":[\"122365\"],\"state\":[\"finished\"],\"requestMerchantID\":[\"122365\"],\"processMerchantID\":[\"122365\"],\"xref\":[\"20071011VC04BK02GL91LHZ\"],\"transactionID\":[\"69398355\"],\"timestamp\":[\"2020-07-10 11:04:02\"],\"vcsResponseCode\":[\"0\"],\"vcsResponseMessage\":[\"Success - no velocity check rules applied\"],\"currencyExponent\":[\"2\"],\"merchantID2\":[\"122365\"],\"reference\":[\"60c40eab-c1ff-431d-86ac-51a1dcd099cf\"]}",
    #         "attributes": {
    #             "ApproximateReceiveCount": "1",
    #             "SentTimestamp": "1575475031083",
    #             "SenderId": "AKIA4T2RH2EKQWEICEFX",
    #             "ApproximateFirstReceiveTimestamp": "1575475031089"
    #         },
    #         "messageAttributes": {},
    #         "md5OfBody": "e7dfba465de78617df5d0752c74f5297",
    #         "eventSource": "aws:sqs",
    #         "eventSourceARN":
    #             "arn:aws:sqs:eu-west-2:389139102731:dev-application-created",
    #         "awsRegion": "eu-west-1"
    #     }
    #     ]
    # }

    event = {
        "Records": [{
            "messageId": "6abd8bca-da4d-4e80-9260-c64953a4383e",
            "receiptHandle":
                "AQEB7b3pJbecFIFjILb5kV3y4OFcqTnRyqtuYppoutcDHfXzCvi7E6aoSHT/LPI49kkCsxZrPyiteDL+Pk7hvwgWPLd1G8YsIsuD0eQ58HyH6WNuNqAK9h0aah6GTYChNJtKAOC1d/5sgU/vyOOWvQqyw6ts3KTDjBA88IFEfwNhFrSscLOabZl1PYmMtH0vvi8S4VpwbLrnEewOb++XNbCYdSfEaPj6K4kZFwKgiH994LEH47wBlYGaebMEKa+ODqfXVx96ry5pFUbWcMzPE1s7V1qW7ldY5999q/703VMVM1fCb7Gll1AF97sv0BX0QbKcgxnfo6C9UIX5gMoa33WNPGwG38s3Ieg86TB0xR7UgN5Yktu1WPm6EmR5feCtkRwXbTamKkuEMRzbnnZnFw4ufw==",
            "body":
                "{\"merchantID\":[\"122365\"],\"threeDSEnabled\":[\"N\"],\"avscv2CheckEnabled\":[\"Y\"],\"riskCheckEnabled\":[\"N\"],\"caEnabled\":[\"Y\"],\"rtsEnabled\":[\"Y\"],\"cftEnabled\":[\"N\"],\"threeDSCheckPref\":[\"not known,not checked,authenticated,not authenticated,attempted authentication\"],\"cv2CheckPref\":[\"not known,not checked,matched,not matched,partially matched\"],\"addressCheckPref\":[\"not known,not checked,matched,not matched,partially matched\"],\"postcodeCheckPref\":[\"not known,not checked,matched,not matched,partially matched\"],\"cardCVVMandatory\":[\"Y\"],\"customerReceiptsRequired\":[\"N\"],\"eReceiptsEnabled\":[\"N\"],\"eReceiptsStoreID\":[\"1\"],\"merchantCategoryCode\":[\"5968\"],\"surchargeEnabled\":[\"N\"],\"__wafRequestID\":[\"2020-07-13T10:49:46Z|e859f296b7|35.179.78.6|OI2j6arV0W\"],\"action\":[\"VERIFY\"],\"amount\":[\"0\"],\"type\":[\"1\"],\"countryCode\":[\"826\"],\"currencyCode\":[\"826\"],\"cardExpiryMonth\":[\"06\"],\"cardExpiryYear\":[\"23\"],\"transactionUnique\":[\"12345678\"],\"orderRef\":[\"12345678\"],\"customerName\":[\"Anna Testowa\"],\"customerEmail\":[\"annatestowa@gmail.com\"],\"customerPhone\":[\"07912345678\"],\"customerAddress\":[\"36 Oxgate Gardens\"],\"customerPostcode\":[\"NW2 6EB\"],\"requestID\":[\"5f0c3c4a42dd9\"],\"merchantAlias\":[\"122365\"],\"responseCode\":[\"0\"],\"responseMessage\":[\"ACCOUNT VALID\"],\"state\":[\"verified\"],\"requestMerchantID\":[\"122365\"],\"processMerchantID\":[\"122365\"],\"paymentMethod\":[\"card\"],\"cardType\":[\"Visa Debit\"],\"cardTypeCode\":[\"VD\"],\"cardScheme\":[\"Visa\"],\"cardSchemeCode\":[\"VC\"],\"cardIssuer\":[\"BARCLAYS BANK PLC\"],\"cardIssuerCountry\":[\"United Kingdom\"],\"cardIssuerCountryCode\":[\"GBR\"],\"cardFlags\":[\"8323329\"],\"cardNumberMask\":[\"465860******8010\"],\"cardNumberValid\":[\"Y\"],\"xref\":[\"20071311WD49TH46MP93FFQ\"],\"cardExpiryDate\":[\"0623\"],\"authorisationCode\":[\"050947\"],\"transactionID\":[\"69681218\"],\"responseStatus\":[\"0\"],\"timestamp\":[\"2020-07-13 11:49:47\"],\"amountApproved\":[\"0\"],\"amountReceived\":[\"0\"],\"avscv2ResponseCode\":[\"244000\"],\"avscv2ResponseMessage\":[\"SECURITY CODE MATCH ONLY\"],\"avscv2AuthEntity\":[\"not known\"],\"cv2Check\":[\"matched\"],\"addressCheck\":[\"not matched\"],\"postcodeCheck\":[\"not matched\"],\"vcsResponseCode\":[\"0\"],\"vcsResponseMessage\":[\"Success - no velocity check rules applied\"],\"acquirerTransactionID\":[\"03P006ECAA7\"],\"acquirerResponseCode\":[\"00\"],\"acquirerResponseMessage\":[\"Authorised\"],\"currencyExponent\":[\"2\"],\"merchantID2\":[\"122365\"],\"signature\":[\"616b50b40a5d50e8b651fab520d4420a0752ea90d0f740d719519c7ee8ec65864ee1fea65aae90d0698716b027ad4ce1e607b57d9e8588356a0ae62f512fe8c5\"],\"reference\":\"60c40eab-c1ff-431d-86ac-51a1dcd099cf\",\"userName\":\"12345678\"}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1575475031083",
                "SenderId": "AKIA4T2RH2EKQWEICEFX",
                "ApproximateFirstReceiveTimestamp": "1575475031089"
            },
            "messageAttributes": {},
            "md5OfBody": "e7dfba465de78617df5d0752c74f5297",
            "eventSource": "aws:sqs",
            "eventSourceARN":
                "arn:aws:sqs:eu-west-2:389139102731:dev-application-created",
            "awsRegion": "eu-west-1"
        }
        ]
    }


    event = {"data":
                 "{\"title\":\"Mr\",\"firstName\":\"John\",\"middleName\":\"Bob\",\"lastName\":\"Doe\",\"email\":\"whatever@gmail.com\",\"mobilePhone\":\"07912345678\",\"address1\":\"666 Whatever Street\",\"postcode\":\"A1 B2C\",\"cardNumber\":\"4242424242424242\",\"cardExpirationYear\":2021,\"cardExpirationMonth\":1,\"cardSecurityNumber\":\"123\",\"userName\":\"12345678\",\"reference\":\"60c40eab-c1ff-431d-86ac-51a1dcd099cf\"}"}

try:
    context = sys.argv[2]
except IndexError:
    context = "{}"

lambda_function.lambda_handler(event, context)