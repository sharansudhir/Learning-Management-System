import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid

USER_POOL_ID = 'us-east-1_DGGPKQbKi'
CLIENT_ID = '38a249j46kf8u2pcsrvubc00eo'
CLIENT_SECRET = '2qslgum57540ntqnldqeh5q377e52h1rq1km16icrbed80t2tub'

def get_secret_hash(username):
    message = username + CLIENT_ID
    digraph = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        message = str(message).encode('utf-8'),
        digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(digraph).decode()
    return d2
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    try:
        username = event['username']
        response = client.resend_confirmation_code(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
    )
    except client.exceptions.UserNotFoundException:
        return {"error": True, "success": False, "message":   "Username doesnt exists"}
        
    except client.exceptions.InvalidParameterException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
      
    return  {"error": False, "success": True}
