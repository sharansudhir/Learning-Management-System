import json
import boto3
import urllib.parse

s3 = boto3.resource('s3')
comprehend = boto3.client(service_name='comprehend')

def lambda_handler(event, context):
    obj = s3.Object("projectsetniment","message.json")
    data = obj.get()['Body'].read().decode()
    text=json.loads(data)
    print(text)
    list = []
    

    for message in text:
        print(message)
        dict = {}
        message_text = message['message']
        sentiment=comprehend.detect_sentiment(Text=message_text,LanguageCode='en')['Sentiment']
        dict['sender_id'] = message['sender_id']
        dict['text'] = message_text
        dict['sentiment'] = sentiment
        list.append(dict)
    
    print(list)
        
    with open("/tmp/" +'message_tagged.json', 'w') as json_file:
        json.dump(json.dumps(list), json_file)
    # uploading a file to the s3 bucket
    
    s3_client = boto3.client('s3')
    
    s3_client.upload_file("/tmp/" + 'message_tagged.json','taggedsentiments', 'message_tagged.json')
    
    #s3.put_object(Body=json.dumps(list), Bucket='taggedsentiments', Key='message_tagged.json') 
   

    #s3.Bucket('taggedsentiments').put_object(Key='message_tagged.json', Body=json.dumps(list))
   
