from google.cloud import storage
import json
from flask import jsonify

def hello_world(request):
    
    if request.method == 'OPTIONS':
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            print("options")
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)

    if request.method == "GET":
        print("get called")
        try:
            storage_client = storage.Client()

            bucket = storage_client.bucket('chat-module')
            blob = bucket.blob('message.json')
            blob.download_to_filename("/tmp/message.json")

            f=open("/tmp/message.json", "r")
            # with open("/tmp/message.json", 'r') as file:
            contents = f.read()  

            print(type(contents))
            print(contents)

            x = json.dumps(contents)
            print(type(x))


            headers = {'Access-Control-Allow-Origin': '*'}

            return (x, 200, headers)
        except:
            print (not Ok)

