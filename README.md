![](tinyauthlogo.png)

tinyauth is a very tiny passwordless GraphQL authentication service. tinyauth keeps authentication simple with 3 easy steps.

## Step 1

- sends code to user's phone

```graphql
mutation {
  sendVerification(phone: "+15559993478") {
    status # 200
    message # verification sent
    success # true
  }
}
```

## Step 2

- verify phone with code user received as sms

```graphql
mutation {
  verifyUser(verification: { phone: "+15559993478", code: "555555" }) {
    status
    message
    success
    auth # auth jwt to include in future headers
  }
}
```

## Step 3

- place jwt in headers {"auth": "auth-jwt-from-last-step"}

- run the `getMe` query

```graphql
{
  getMe {
    id
    phone
  }
}
```

### Develop

Set up your .aws credentials, make a DynamoDB table named tinyauth-dev

Install node (to run serverless-offline). I use nvm to manage my node versions.

Go to your tinyauth-api folder:

`touch .env`

Add TABLE_NAME and API_SECRET environment variables.

```console
TABLE_NAME=my-app-dev
API_SECRET=somethingsecret
```

`npm install`

`virtualenv -p python3 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`sls deploy` - will automatically make your dynamodb table on aws.

`sls wsgi serve -p 8000` or `yarn run start`

Run queries in Graphi at http://localhost:8000/graphql

### Run Tests

`TABLE_NAME=tinyauth-test API_SECRET=somethingsecret python -m pytest` or `yarn run test`

### Deploy

Update your table name / secret in .env and run

```console
sls deploy
```

### No GraphQL Client?

#### Send verification

```python
import requests

variables = {'phone': '+155555555555'}
mutation = """
mutation SendVerification($phone: String!) {
  sendVerification(phone: $phone) {
    status
    message
    success
  }
}
"""

# or localhost:8000 for dev
requests.post('https://tinyauth.io/graphql', json={'query': mutation, 'variables': variables})
```

#### Verify user

```python
import requests

variables = {'phone': '+155555555555', 'code': '555555'}
mutation = """
mutation VerifyUser($phone: String!, $code: String!) {
  verifyUser(verification: { phone: $phone, code: $code }) {
    status
    message
    success
    auth # auth jwt to include in future headers
  }
}
"""

# or localhost:8000 for dev
requests.post('https://tinyauth.io/graphql', json={'query': mutation, 'variables': variables})
```

#### Get Me

```python
import requests

headers = {
  "auth": your-tinyauth-jwt
}

query = """
{
  getMe {
    id
    phone
  }
}
"""

# or localhost:8000 for dev
requests.post('https://tinyauth.io/graphql', json={'query': query}, headers=headers)
```
