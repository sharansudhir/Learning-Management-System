import json
import boto3
import mysql.connector

def lambda_handler(event, context):
    username = event['username']
    print(username)
    mydb = mysql.connector.connect(
    host="lms-db.cc2g7twee7b3.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Ujwal123",
    database="lms"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM user_details where email=\""+username+"\"")
    myresult = mycursor.fetchall()
    result_json={}
    for x in myresult:
        result_json={'email':x[0],'university':x[3],'name':x[1],'status':x[4],'token':x[5],'role':x[6]}
    mydb.commit()
    return result_json