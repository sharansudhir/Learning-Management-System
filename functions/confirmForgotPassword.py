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
    myDigest = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(message).encode('utf-8'),   digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(myDigest).decode()
    return d2
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    try:
        username = event['username']
        password = event['password']
        code = event['code']
        client.confirm_forgot_password(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            ConfirmationCode=code,
            Password=password,
           )
    except client.exceptions.UserNotFoundException as e:
        return {"error": True, 
                "success": False,
                "data":  None,
                "message": "Username doesnt exists"}
        
    except client.exceptions.CodeMismatchException as e:
        return {"error": True, 
               "success": False,
               "data": None,
               "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException as e:
        return {"error": True, 
                 "success": False, 
                 "data": None, 
                 "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, 
                "success": False,
                "data": None,
                "message": f"Unknown error {e.__str__()} "}
      
    return {"error": False, 
            "success": True, 
            "message": f"Password has been changed successfully",
            "data": None}