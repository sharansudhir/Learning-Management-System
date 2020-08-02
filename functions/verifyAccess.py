import json
import boto3
import hmac
import hashlib
import base64
import mysql.connector

USER_POOL_ID = 'us-east-1_DGGPKQbKi'
CLIENT_ID = '38a249j46kf8u2pcsrvubc00eo'
CLIENT_SECRET = '2qslgum57540ntqnldqeh5q377e52h1rq1km16icrbed80t2tub'
client = None

def get_secret_hash(username):
    message = username + CLIENT_ID
    myDigest = hmac.new(str(CLIENT_SECRET).encode('utf-8'), msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    dec = base64.b64encode(myDigest).decode()
    return dec
def initiate_auth(username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None
    
    
def refresh_auth(username, refresh_token):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
                'SECRET_HASH': get_secret_hash(username)
            },
            ClientMetadata={
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None
def lambda_handler(event, context):
    try:
        mydb = mysql.connector.connect(
        host="lms-db.cc2g7twee7b3.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Ujwal123",
        database="lms"
        )

        global client
        if client == None:
            client = boto3.client('cognito-idp')
        username = event['username']
        if 'password' in event:
            resp, msg = initiate_auth(username, event['password'])
        
        if 'refresh_token' in event:
            resp, msg = refresh_auth(username, event['refresh_token'])
        if msg != None:
            return {
                'status': 'fail', 
                'msg': msg
            }
    
        response = {
            'status': 'success',
            'id_token': resp['AuthenticationResult']['IdToken']
        }
    
        if 'password' in event:
            response['refresh_token'] = resp['AuthenticationResult']['RefreshToken']
        mycursor = mydb.cursor()
        mysql_query="update user_details set status=1 ,token=\""+resp['AuthenticationResult']['IdToken']+"\" where email=\""+username+"\""
        print(mysql_query)
        mycursor.execute(mysql_query)
        mydb.commit()
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
    
    return response