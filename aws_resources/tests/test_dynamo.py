from aws_resources.dynamo import table

def test_table():
    db = table()
    assert db != None
