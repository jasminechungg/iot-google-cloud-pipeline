import base64
import json
import functions_framework
from google.cloud import firestore


# Initialize Database
db = firestore.Client()


@functions_framework.cloud_event
def subscribe(cloud_event):
    try:
        # 1. Decode the message
        pubsub_message = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        print(f"DEBUG: Received Message: {pubsub_message}")
       
        # 2. Parse JSON
        json_data = json.loads(pubsub_message)
       
        # 3. Add Logic (Status Check)
        if json_data.get('temp', 0) > 30.0:
            json_data['status'] = "HOT"
        else:
            json_data['status'] = "OK"


        # 4. Add Timestamp 
        json_data['timestamp'] = firestore.SERVER_TIMESTAMP
       
        # 5. Print Debug Info (UPDATED NAME HERE)
        print(f"DEBUG: Saving to Project: {db.project}")
        print(f"DEBUG: Saving to Collection: data_logs")
       
        # 6. Save to Firestore (UPDATED NAME HERE)
        # This creates the new collection 'data_logs' automatically
        update_time, ref = db.collection('data_logs').add(json_data)
       
        print(f"SUCCESS! Created Document ID: {ref.id}")
       
    except Exception as e:
        print(f"ERROR: {e}")


