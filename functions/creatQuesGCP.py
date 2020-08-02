from google.cloud import firestore
import json 

def create_ques(request):
    db = firestore.Client()
    doc_error={'success':'False','Error':'True'}
    doc_success={'success':'True','Error':'False'}
    request_json = request.get_json()
    if 'email' and 'ques1' and 'ques2' and 'ques3' in request_json:
        try:
            doc_ref = db.collection('users').document(request_json['email'])
            doc = doc_ref.set({request_json['ques1']:request_json['ans1'],request_json['ques2']:request_json['ans2'],request_json['ques3']:request_json['ans3']})
            #return f'{doc_success}'
            return json.dumps(doc_success)
        except Exception as e:
            #return f'{doc_error}'
            return json.dumps(doc_error)
    else:
        #return f'{doc_error}'
        return json.dumps(doc_error)
