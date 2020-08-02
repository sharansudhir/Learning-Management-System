from google.cloud import pubsub_v1
from google.cloud import storage
import json
import os

def hello_pubsub(event, context):
    try:

        # print("line 1")
        proj_id = "serverless-project-284322"
        sub_id = "recieve_message"
        ack=[]
        # print("line 2")
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(proj_id, sub_id)
        # print('line 3')
        response = subscriber.pull(subscription_path, max_messages=5)
        content = []
        for msg in response.received_messages:
            x = msg.message.data.decode("utf-8")
            x = json.loads(x)
            content.append(x)
            print("Received message:",x)

        ack_ids = [msg.ack_id for msg in response.received_messages]
        subscriber.acknowledge(subscription_path, ack_ids)
        
        storage_client = storage.Client()

        bucket = storage_client.bucket('chat-module')
        blob = bucket.blob('message.json')
        blob.download_to_filename("/tmp/message.json")

        if(os.stat("/tmp/message.json").st_size == 0):
            mess = []
            mess.append(x)
            with open('/tmp/message.json','w') as json_file:
                json.dump(mess,json_file)
        else:
            with open('/tmp/message.json',"r") as json_file:
                data = json.load(json_file)
            
            print(data)

            data.append(x)

            with open('/tmp/message.json','w') as json_file:
                json.dump(data,json_file)

        source = 'message.json'
        destination = 'message.json'
        storage_client = storage.Client()
        bucket = storage_client.bucket('chat-module')
        blob = bucket.blob(destination)

        blob.upload_from_filename("/tmp/message.json")
    
    except Exception as e:
        print(str(e)) 


  


