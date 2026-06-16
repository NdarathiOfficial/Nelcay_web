import os
import json
import firebase_admin
from firebase_admin import credentials

# Fetch the JSON string from Environment Variables
firebase_json_str = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
firebase_dict = json.loads(firebase_json_str)

cred = credentials.Certificate(firebase_dict)
firebase_admin.initialize_app(cred)