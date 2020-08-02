import json
import boto3
import hmac
import hashlib
import base64
import mysql.connector


def lambda_handler(event, context):
    try:
        username = event['username']
        mydb = mysql.connector.connect(
        host="lms-db.cc2g7twee7b3.us-east-1.rds.amazonaws.com",
        user="admin",
        password="Ujwal123",
        database="lms"
        )
        mycursor = mydb.cursor()
        mysql_query="update user_details set status=0 ,token=\"\" where email=\""+username+"\""
        print(mysql_query)
        mycursor.execute(mysql_query)
        mydb.commit()
    except Exception as e:
        return {"error": True, "success": False, "message": f"Unknown error {e.__str__()} "}
        
    
    return {"error": False, "success": True, "message": "Session Terminated"}
     
