from google.cloud import firestore
import json 
def get_ques(request):
    db = firestore.Client()
    doc_error = {'success':'False','error':'True'}
    request_json = request.get_json()
    if 'email' in request_json:
        try:
            doc_ref = db.collection('users').document(str(request_json['email']))
            doc = doc_ref.get()
            if doc.exists:
                print(f'Document data: {doc.to_dict()}')
                #return f'{doc.to_dict()}'
                return json.dumps(doc.to_dict())
            else:
                return json.dumps(doc_error)
        except Exception as e:
            return json.dumps(doc_error)
    else:
        return json.dumps(doc_error)
