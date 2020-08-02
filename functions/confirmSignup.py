import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import mysql.connector

USER_POOL_ID = 'us-east-1_DGGPKQbKi'
CLIENT_ID = '38a249j46kf8u2pcsrvubc00eo'
CLIENT_SECRET = '2qslgum57540ntqnldqeh5q377e52h1rq1km16icrbed80t2tub'

def get_secret_hash(username):
    message = username + CLIENT_ID
    myDigest = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        message = str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(myDigest).decode()
    return d2
    
def lambda_handler(event, context):
    mydb = mysql.connector.connect(
    host="lms-db.cc2g7twee7b3.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Ujwal123",
    database="lms"
    )
    client = boto3.client('cognito-idp')
    try:
        username = event['username']
        password = event['password']
        code = event['code']
        name = event['name']
        role = event['role']
        university = event['university']
        response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
        ConfirmationCode=code,
        ForceAliasCreation=False,
       )
        mycursor = mydb.cursor()
        mysql_query="insert into user_details(email,password,university,name,role) values (%s,%s,%s,%s,%s)"
        values=(username,password,university,name,role)
        mycursor.execute(mysql_query,values)
        mydb.commit()
    except client.exceptions.UserNotFoundException:
        #return {"error": True, "success": False, "message": "Username doesnt exists"}
        return event
    except client.exceptions.CodeMismatchException:
        return {"error": True, "success": False, "message": "Invalid Verification code"}
        
    except client.exceptions.NotAuthorizedException:
        return {"error": True, "success": False, "message": "User is already confirmed"}
    
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}

    return event