from aws_resources.dynamo import table
from features.Users.user import send_verification, verify_user, get_me
from moto import mock_dynamodb2, mock_sns
import boto3
from aws_resources.mock_dynamo import setup_mocks, phone, mock_verification
import jwt
import os

@mock_dynamodb2
@mock_sns
def test_send_verification():
    setup_mocks()
    client = boto3.client("sns", region_name="us-east-1")
    client.create_topic(Name="some-topic")
    resp = client.create_topic(Name="some-topic")
    arn = resp["TopicArn"]
    client.subscribe(TopicArn=arn, Protocol="sms", Endpoint=phone)
    resp = send_verification(None, None, phone)
    assert resp['code'] == 200

@mock_dynamodb2
def test_verify_user():
    setup_mocks()
    table().put_item(Item=mock_verification)
    resp = verify_user(None, None, {'phone': phone, 'code': '123456'})
    assert resp['code'] == 200
    assert resp['auth'] != None

class MockObject():
    pass


@mock_dynamodb2
def test_get_me():
    setup_mocks()
    user = {
        'pk': 'user#123',
        'sk': phone,
    }
    table().put_item(Item=user)
    auth = jwt.encode(user, os.environ['API_SECRET'], algorithm='HS256')
    token = auth.decode('utf8')
    info = MockObject
    info.context = MockObject
    info.context.headers = {"Auth": token}
    resp = get_me(None, info)
    assert resp['id'] == '123'
    assert resp['phone'] == phone