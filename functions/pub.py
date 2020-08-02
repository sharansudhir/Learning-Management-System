import os
from google.cloud import pubsub_v1
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

    if request.method == "POST":
        print("post called")
        try:
            testAttribute = request.get_json()
            print(type(testAttribute))
            # timestamp = time.time()
            # testAttribute = json.loads(testAttribute)
            # testAttribute['timestamp'] = timestamp
            testAttribute = json.dumps(testAttribute)
            data = testAttribute.encode("utf-8")
            proj_id = "serverless-project-284322"
            topic_id = "pub-sub-message"
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(proj_id, topic_id)
            # print(testAttribute)
            # publisher.publish(topic_name, b'', testAttribute=testAttribute)
            headers = {
            'Access-Control-Allow-Origin': '*'
            }

            r = jsonify({"result": "Received Successfully"})
            return (r, 200, headers)
        except:
            return f"Not OK"
