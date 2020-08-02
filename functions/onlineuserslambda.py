#Code used for fetching online users in lex bot
#Code adopted from Lambda blueprints provided in AWS Educate account - lex-order-flowers-python


import math
import dateutil.parser
import datetime
import time
import os
import logging
import pymysql

host = "lms-db.cc2g7twee7b3.us-east-1.rds.amazonaws.com"
port = 3306
dbname = "lms"
user = "admin"
password = "Ujwal123"
connection = pymysql.connect(host, user=user, port=port, password=password, db=dbname)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response





def online_users(intent_request):
   

    help = get_slots(intent_request)["help"]
    orgname = get_slots(intent_request)["online"]
    print(orgname)
    users=[]
    cursor=connection.cursor()
    sql_fecth = "SELECT name FROM lms.user_details where university=%s and status=1;"
    cursor.execute(sql_fecth, orgname)
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
        users.append(row[0])
        
    
    
 
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'List of online user:'+', '.join(users)})


def dispatch(intent_request):
    

    intent_name = intent_request['currentIntent']['name']

    
    if intent_name == 'onlineusers':
        return online_users(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
   
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
