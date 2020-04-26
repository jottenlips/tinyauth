from aws_resources.dynamo import table
from boto3.dynamodb.conditions import Key
import uuid
import jwt
import boto3
import os 
from random import randint
import time
import phonenumbers

def get_me(obj, info):
    request = info.context
    token = request.headers["Auth"]
    values = jwt.decode(token, os.environ['API_SECRET'], algorithm='HS256')
    user = table().query(
        KeyConditionExpression=f'pk = :pk AND sk = :sk',
        ExpressionAttributeValues={
            ':pk': values['pk'],
            ':sk': values['sk']
        }
    )['Items'][0]

    return {
        'id': user['pk'].split('#')[1],
        'phone': user['sk']
    }

def delete_code(phone, code):
    return table().delete_item(Key={
        'pk': phone,
        'sk': f'verificationCode#{code}'
    })

def delete_old_codes(phone):
    old_codes = table().query(
        KeyConditionExpression=f'pk = :pk AND begins_with(sk, :sk)',
        ExpressionAttributeValues={
            ':pk': phone,
            ':sk': 'verificationCode#'
        }
    )['Items']
    if (len(old_codes) > 0):
        return [delete_code(phone, code['sk'].split('#')[1]) for code in old_codes]

def send_verification(obj, info, phone):

    try:
        number = phonenumbers.parse(phone, None)
        e164_number  = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        if not phonenumbers.is_valid_number(number):
            return {
                'message': f'Phone number is not E164',
                'status': 400,
                'success': False
            }
    except Exception as e: 
        return {
            'message': f'Phone number is not E164',
            'status': 400,
            'success': False
        }

    delete_old_codes(phone)
    id = str(uuid.uuid4())
    verification_code = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])

    verification = {
        'pk': phone,
        'sk': f'verificationCode#{verification_code}',
        'expiration': str(int(time.time() + 1200))
    }
    # check for phone number
    table().put_item(Item=verification)
    client = boto3.client(
        "sns",
        region_name="us-east-1"
    )
    client.publish(
        PhoneNumber = phone,
        Message = f'Hello! your verification code is {verification_code}'
    )
    return {
        'message': 'success',
        'status': 200,
        'success': True
    }

def verify_user(obj, info, verification):

    phone = verification['phone']
    code = verification['code']

    verification_query = table().query(
          KeyConditionExpression=f'pk = :pk AND begins_with(sk, :sk)',
            ExpressionAttributeValues={
                ':pk': phone,
                ':sk': f'verificationCode#{code}'
            }
    )['Items']

    if (len(verification_query) != 0 and int(float(verification_query[0]['expiration'])) > int(time.time())):
        delete_code(phone, code)
        user_from_table = table().query(
            KeyConditionExpression=f'pk = :pk AND begins_with(sk, :sk)',
            ExpressionAttributeValues={
                ':pk': phone,
                ':sk': 'user#'
            }
        )['Items']

        if (len(user_from_table) == 1):
            refreshed_user = table().query(
                KeyConditionExpression=f'pk = :pk AND begins_with(sk, :sk)',
                ExpressionAttributeValues={
                    ':pk': user_from_table[0]['sk'],
                    ':sk': phone
                }
            )['Items']

            auth = jwt.encode(refreshed_user[0], os.environ['API_SECRET'], algorithm='HS256')
            return {
                'auth': auth.decode("utf-8") ,
                'message': 'success, reauthenticated user',
                'status': 200,
                'success': True
            }

        user_id = str(uuid.uuid4())
        phone_record = {
            'pk': phone,
            'sk': f'user#{user_id}'
        }
        user = {
            'pk': f'user#{user_id}',
            'sk': phone,
        }
        table().put_item(Item=user)
        table().put_item(Item=phone_record)
        auth = jwt.encode(user, os.environ['API_SECRET'], algorithm='HS256')
        return {
            'auth': auth.decode("utf-8") ,
            'message': 'success, user created',
            'status': 200,
            'success': True
        }
    return {
        'message': 'not found',
        'status': 400,
        'success': True
    }