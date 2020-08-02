import json
import boto3
import hmac
import hashlib
import base64

USER_POOL_ID = 'us-east-1_DGGPKQbKi'
CLIENT_ID = '38a249j46kf8u2pcsrvubc00eo'
CLIENT_SECRET = '2qslgum57540ntqnldqeh5q377e52h1rq1km16icrbed80t2tub'
client = None

def get_secret_hash(username):
    message = username + CLIENT_ID
    myDigest = hmac.new(str(CLIENT_SECRET).encode('utf-8'), message=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    dec = base64.b64encode(myDigest).decode()
    return dec
    
def create_auth(username, password,name,email):
    try:
        result = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
            {
                'Name': "name",
                'Value': name
            },
            {
                'Name': "email",
                'Value': email
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            }
        ])
    except client.exceptions.UsernameExistsException as e:
        return {"error": False, 
               "success": True, 
               "message": "This username already exists", 
               "data": None}
    except client.exceptions.InvalidPasswordException as e:
        
        return {"error": False, 
               "success": True, 
               "message": "Password should have Caps,\
                          Special chars, Numbers", 
               "data": None}
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False, 
               "success": True, 
               "message": "Email already exists", 
               "data": None}
    
    except Exception as e:
        return {"error": False, 
                "success": True, 
                "message": str(e), 
               "data": None}
    
    return {"error": False, 
            "success": True, 
            "message": "Success, Enter OTP", 
            "data": None}
            

 
def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    username = event['username']
    password = event['password']
    name = event['name']
    email = event['email']


    return create_auth(username,password,name,email)
 