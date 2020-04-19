
from moto import mock_dynamodb2
import boto3
import os 
import time

phone = "+15551234567"

mock_verification = {
    'pk': phone,
    'sk': 'verificationCode#123456',
    'expiration': str(int(time.time() + 1200))
}

@mock_dynamodb2
def setup_mocks():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName= os.environ['TABLE_NAME'],
        KeySchema=[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'  # primary key
            },
              {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'  # primary key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            },
        ],
    )